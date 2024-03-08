import json

import pytz
from datetime import datetime, timedelta

from odoo import http, _
from odoo.http import request, Controller

from .service_siat_sync import ServiceSiatSync
from . import service_invoices
from ..models.event import Event
from ..models.package import Package
from ..libsiat.classes.siat_factory import SiatFactory
from ..libsiat import functions as siat_functions
from ..libsiat import constants as siat_constants
from ..libsiat.services.service_operaciones import ServiceOperaciones
from ..libsiat.classes.siat_exception import SiatException

class ServiceSiatEvents(ServiceSiatSync):
	
	def __init__(self):
		super().__init__()

	def eventoActivo(self, sucursal=0, puntoventa=0):
	
		items = request.env['siat.event'].search([
			('sucursal_id', '=', sucursal),
			('puntoventa_id', '=', puntoventa),
			('status', '=', Event.STATUS_OPEN),
		], limit=1)
		
		if len(items) <= 0:
			return None
			
		return items[0]

	def create(self, data: dict):

		sucursal = int(data.get('sucursal_id', 0))
		puntoventa = int(data.get('puntoventa_id', 0))
		if sucursal < 0:
			raise Exception('Codigo sucursal invalido')
		if puntoventa < 0:
			raise Exception('Codigo sucursal invalido')
			
		if self.eventoActivo(sucursal, puntoventa) is not None:
			raise Exception('Ya existe un evento activo para la sucursal y punto de venta')
			
		if not data.get('fecha_inicio', ''):
			raise Exception('Fecha de inicio del evento invalida')
		
		fecha_inicio 	= siat_functions.sb_siat_parse_datetime(data['fecha_inicio'].replace('Z', ''))
		fecha_fin		= None
		cufd_evento		= None
		
		if data.get('evento_id', 0) <= 0:
			raise Exception('Codigo de evento invalido')
		
		evento_siat = self.buscar_evento(data['evento_id'])
		if evento_siat is None:
			raise Exception('El codigo de evento no existe, no se puede registrar el evento')
		
		if 	data.get('evento_id') <= 4:
			current_cufd	= self.sync_cufd(data.get('sucursal_id', 0), data.get('puntoventa_id', 0))
			cufd_evento 	= current_cufd.codigo
			
		
		if data.get('evento_id') > 4:
			if not data.get('fecha_fin'):
				raise Exception('Debe seleccionar una fecha fin para el evento de contingencia')
			
			cufd_evento = data.get('cufd_evento')
			fecha_fin = siat_functions.sb_siat_parse_datetime(data['fecha_fin'].replace('Z', ''))
		
		if not cufd_evento:
			raise Exception('CUFD para el evento invalido')
		
		if not request.env['siat.cufd'].getByCode(cufd_evento):
			raise Exception('El CUFD no existe o es invalido')
		
		event_data = {
			'evento_id': data.get('evento_id'),
			'sucursal_id': data.get('sucursal_id', 0),
			'puntoventa_id': data.get('puntoventa_id', 0),
			'descripcion': evento_siat.get('descripcion'),
			'cufd_evento': cufd_evento,
			'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
			'fecha_fin': None if not fecha_fin else fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
			'status': Event.STATUS_OPEN,
			'company_id': request.env.company.id
		}
		print('EVENT DATA: ', event_data)
		
		event = request.env['siat.event'].create(event_data)

		return event

	def read(self, id):
		event = request.env['siat.event'].browse(id)
		
		if event is None or len(event) <= 0:
			return None
			
		return event[0]
		
	def close(self, event_id):
		
		event = self.read(event_id)
		if event is None:
			raise Exception('El evento no existe, no se puede cerrar')
		
		if event.status == Event.STATUS_CLOSED:
			raise Exception('El evento ya se encuentra cerrado')
			
		evento_siat = self.buscar_evento(event.evento_id)
		if evento_siat is None:
			raise Exception('El codigo de evento no existe, no se puede registrar el evento')

		invoices = event.get_pending_invoices()
		if len( invoices ) <= 0:
			event.write({'status': Event.STATUS_CLOSED})
			return event

		cuis = self.sync_cuis(event.sucursal_id, event.puntoventa_id)
		cufd = self.sync_cufd(event.sucursal_id, event.puntoventa_id)

		if not event.codigo_reception:
			fecha_fin = None
			if event.evento_id < 5:
				fecha_fin = siat_functions.sb_siat_localize_datetime(datetime.now())
			else:
				fecha_fin = event.fecha_fin

			# try to renew the CUFD
			if event.cufd_evento == cufd.codigo:
				cufd = self.sync_cufd(event.sucursal_id, event.puntoventa_id, 1)

			serviceOps = ServiceOperaciones()
			serviceOps.setConfig(self.getConfig())
			serviceOps.cuis = cuis.get('codigo')
			serviceOps.cufd = cufd.codigo
			serviceOps.debug = True

			res = serviceOps.registroEventoSignificativo(
				evento_siat['codigoClasificador'],
				evento_siat['descripcion'],
				event.cufd_evento,
				event.fecha_inicio,
				fecha_fin,
				event.sucursal_id,
				event.puntoventa_id
			)
			print(res)
			if not res['codigoRecepcionEventoSignificativo'] or res['transaccion'] is False:
				# error = siat_functions.sb_siat_response_message(res)
				raise SiatException(res)

			event.write({
				'cufd': cufd.codigo,
				'fecha_fin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
				'codigo_reception': res['codigoRecepcionEventoSignificativo']
			})

		serviceInvoices = service_invoices.ServiceInvoices()
		service = SiatFactory.obtenerServicioFacturacion(
			self.getConfig(),
			cuis.get('codigo'),
			cufd.codigo,
			cufd.codigo_control
		)
		service.debug = True

		packages = event.get_packages()
		for pkg in packages:
			# if pkg.status != Package.STATUS_OPEN:
			if pkg.status in [Package.STATUS_CLOSED]:
				continue

			invoices = pkg.get_pending_invoices()
			siatInvoices = []
			for invoice in invoices:
				siatInvoice = serviceInvoices.invoiceToSiatInvoice(invoice)
				print( siatInvoice.toXmlString() )
				siatInvoices.append( siatInvoice )

			if len( siatInvoices ) <= 0 :
				continue

			data = {'reception': None, 'reception_error': None}
			res = service.recepcionPaqueteFactura(
				siatInvoices,
				event.codigo_reception,
				siat_constants.TIPO_EMISION_OFFLINE,
				pkg.invoice_type,
				None
			)
			print('RECEPCION PAQUETE',  res)

			if res.get('codigoEstado') != 901: # PENDIENTE
				data['reception_error'] = res
			else:
				data['reception'] = res

			pkg.write({
				'status': Package.STATUS_PENDING if res.get('codigoEstado', 0) == 901 else Package.STATUS_OPEN,
				'reception_code': res.get('codigoRecepcion', None),
				'reception_status': res.get('codigoDescripcion'),
				'reception_date': datetime.now(),
				'data': json.dumps(data)
			})

			# if res.get('codigoEstado') == 901: # != 901:
			#	#raise SiatException(siat_functions.sb_siat_response_message(res))
			#	self.verify_package(pkg)

		self.verify_event_reception(event)

		return event

	def verify_event_reception(self, event: Event):
		verified = True
		if not event.codigo_reception:
			raise Exception('El evento no tiene codigo de recepcion, no se puede verificar')

		for pkg in event.get_packages():
			_pkg = self.verify_package(pkg)
			if _pkg.status != Package.STATUS_CLOSED:
				verified = False

		if verified:
			event.write({
				'status': Event.STATUS_CLOSED
			})

		return event

	def verify_package(self, package: Package):
		_max_tries_ = 50

		if not package.reception_code:
			raise Exception('El paquete "id:{0}" no tiene codigo de recepcion, no de puede validar'.format(package.id))

		if package.status == Package.STATUS_CLOSED:
			return package

		cuis = self.sync_cuis(package.event_id.sucursal_id, package.event_id.puntoventa_id)
		cufd = self.sync_cufd(package.event_id.sucursal_id, package.event_id.puntoventa_id)

		service = SiatFactory.obtenerServicioFacturacion(
			self.getConfig(),
			cuis.get('codigo'),
			cufd.codigo,
			cufd.codigo_control
		)
		service.debug = True
		res = service.validacionRecepcionPaqueteFactura(
			package.event_id.sucursal_id,
			package.event_id.puntoventa_id,
			package.reception_code,
			package.invoice_type,
			package.sector_document
		)
		print(res)
		_try_ = 0
		while res['codigoDescripcion'] == 'PENDIENTE':
			res = service.validacionRecepcionPaqueteFactura(
				package.event_id.codigo_sucursal,
				package.event_id.punto_venta,
				package.reception_code,
				package.invoice_type,
				package.sector_document
			)
			_try_ += 1
			if _try_ >= _max_tries_:
				break

		data = package.get_data()
		data['reception'] = res

		package.write({
			'reception_status': res['codigoDescripcion'],
			'status': Package.STATUS_CLOSED if res['codigoDescripcion'] == 'VALIDADA' else Package.STATUS_PENDING,
			'data': json.dumps(data)
		})

		if res['codigoDescripcion'] == 'VALIDADA':
			package.invoices.write({
				'siat_id': package.reception_code,
				# 'tipo_emision': 1,
			})

		return package

	def void(self, id):
		event = self.read(id)
		if event is None:
			raise Exception('El evento no existe, no se puede anular')
		if event.status == Event.STATUS_VOID:
			raise Exception('El evento ya esta anulado')
			
		event.write({'status': Event.STATUS_VOID})
		
		return event
		
