import pytz
import base64
from datetime import datetime, timedelta

from odoo import tools, Command
from odoo.http import request, Controller


from .service_siat import ServiceSiat
from .service_siat_sync import ServiceSiatSync
from .service_siat_events import ServiceSiatEvents
from ..models.invoice import Invoice
from ..models.mail_template import SiatMailTemplate
from ..libsiat.classes.siat_factory import SiatFactory
from ..libsiat import functions as siat_functions
from ..libsiat import constants as siat_constants
from ..libsiat.invoices.siatinvoice import SiatInvoice
from ..libsiat.classes.siat_exception import SiatException, SiatExceptionInvalidNit
import json
from datetime import datetime, timedelta
import re


class ServiceInvoices(ServiceSiat):
	
	def __init__(self):
		
		self.serviceSync = ServiceSiatSync()
		self.serviceEvents = ServiceSiatEvents()
	
	def siatInvoiceToInvoice(self, facturaSiat):
		monto_giftcard = facturaSiat.cabecera.montoGiftCard if facturaSiat.cabecera.montoGiftCard is not None else 0
		#subtotal = facturaSiat.cabecera.montoTotal + monto_giftcard - facturaSiat.cabecera.descuentoAdicional
		subtotal = facturaSiat.cabecera.montoTotal + facturaSiat.cabecera.descuentoAdicional
		total_tax = facturaSiat.cabecera.montoTotal * 0.13
		invoice = {
			'customer_id': 0,
			'invoice_number': facturaSiat.cabecera.numeroFactura,
			'codigo_sucursal': facturaSiat.cabecera.codigoSucursal,
			'punto_venta': facturaSiat.cabecera.codigoPuntoVenta,
			'actividad_economica': 0,
			'codigo_documento_sector': facturaSiat.cabecera.codigoDocumentoSector,
			'tipo_documento_identidad': facturaSiat.cabecera.codigoTipoDocumentoIdentidad,
			'codigo_metodo_pago': facturaSiat.cabecera.codigoMetodoPago,
			'codigo_moneda': facturaSiat.cabecera.codigoMoneda,
			'evento_id': 0,
			'package_id': 0,
			'tipo_factura_documento': 0,
			'ambiente': 2,
			'nit_ruc_nif': facturaSiat.cabecera.numeroDocumento,
			'control_code': '',
			'status': 'ISSUED',
			'cufd': facturaSiat.cabecera.cufd,
			'cuf': facturaSiat.cabecera.cuf,
			'cafc': facturaSiat.cabecera.cafc,
			'complemento': facturaSiat.cabecera.complemento,
			'numero_tarjeta': facturaSiat.cabecera.numeroTarjeta,
			'siat_id': '',
			'tipo_emision': 0,
			'nit_emisor': facturaSiat.cabecera.nitEmisor,
			'leyenda': facturaSiat.cabecera.leyenda,
			'subtotal': subtotal,
			'total_tax': total_tax,
			'discount': facturaSiat.cabecera.descuentoAdicional,
			'monto_giftcard': facturaSiat.cabecera.montoGiftCard,
			'tipo_cambio': facturaSiat.cabecera.tipoCambio,
			'invoice_datetime': datetime.strptime(facturaSiat.cabecera.fechaEmision, siat_constants.DATETIME_FORMAT),
			'total': facturaSiat.cabecera.montoTotal,
			'customer_name': facturaSiat.cabecera.nombreRazonSocial,
			'data': {
				'excepcion': facturaSiat.cabecera.codigoExcepcion,
				'nro_cafc': None
			}
		}
		
		return invoice
	
	def siatDetailToInvoiceDetail(self, invoiceDetail):
		item = {
			'product_id': 0,
			'product_code': invoiceDetail.codigoProducto,
			'codigo_producto_sin': invoiceDetail.codigoProductoSin,
			'unidad_medida': invoiceDetail.unidadMedida,
			'product_name': invoiceDetail.descripcion,
			'codigo_actividad': invoiceDetail.actividadEconomica,
			'numero_seria': '',
			'numero_imei': '',
			'nandina': '',
			'price': invoiceDetail.precioUnitario,
			'quantity': invoiceDetail.cantidad,
			'subtotal': invoiceDetail.precioUnitario * invoiceDetail.cantidad,
			'discount': invoiceDetail.montoDescuento,
			'total': invoiceDetail.subTotal,
		}
		
		return item

	def requestDataToSiatInvoice(self, invoiceData, config):
		facturaSiat = SiatFactory.construirFactura(invoiceData['codigo_documento_sector'], config['modalidad'])
		facturaSiat.cabecera.leyenda = None

		for item in invoiceData['items']:
			if not item.get('codigo_actividad', ''):
				raise Exception(
					'El producto {0} no tiene asignado actividad economica'.format(item.get('product_name')))
			if int(item.get('codigo_producto_sin', 0)) <= 0:
				raise Exception('El producto {0} no tiene asignado codigo SIN'.format(item.get('product_name')))
			if int(item.get('unidad_medida', 0)) <= 0:
				raise Exception(
					'El producto {0} no tiene asignado Unidad de Medida SIN'.format(item.get('product_name')))

			detalleSiat = facturaSiat.instanceDetail()
			detalleSiat.actividadEconomica = item['codigo_actividad']
			detalleSiat.codigoProductoSin = item['codigo_producto_sin']
			detalleSiat.codigoProducto = item['product_code']
			detalleSiat.descripcion = item['product_name']
			detalleSiat.cantidad = item['quantity']
			detalleSiat.unidadMedida = item['unidad_medida']
			detalleSiat.precioUnitario = item['price']
			detalleSiat.montoDescuento = item['discount']
			detalleSiat.subTotal = round(((detalleSiat.cantidad * detalleSiat.precioUnitario) - detalleSiat.montoDescuento), 2)
			detalleSiat.numeroSerie = item.get('numero_serie', '')
			detalleSiat.numeroImei = item['numero_imei']
			if detalleSiat.subTotal <= 0:
				raise Exception(
					'El descuento del item {0} no puede ser igual o mayor al subtotal del detalle agregado '.format(item.get('product_name')))

			facturaSiat.detalle.append(detalleSiat)

			if facturaSiat.cabecera.leyenda is None:
				facturaSiat.cabecera.leyenda = self.serviceSync.leyenda_aleatoria(detalleSiat.actividadEconomica)

		facturaSiat.cabecera.nitEmisor = config['nit']
		facturaSiat.cabecera.razonSocialEmisor = config['razonSocial']
		facturaSiat.cabecera.municipio = config['ciudad']
		facturaSiat.cabecera.telefono = config['telefono']
		facturaSiat.cabecera.numeroFactura = request.env['siat.invoice'].nextInvoiceNumber(invoiceData['company_id'])
		facturaSiat.cabecera.codigoSucursal = invoiceData['codigo_sucursal']
		facturaSiat.cabecera.codigoPuntoVenta = invoiceData['punto_venta']
		facturaSiat.cabecera.nombreRazonSocial = invoiceData['customer']
		facturaSiat.cabecera.codigoTipoDocumentoIdentidad = invoiceData['tipo_documento_identidad']
		facturaSiat.cabecera.numeroDocumento = invoiceData['nit_ruc_nif']
		facturaSiat.cabecera.complemento = invoiceData['complemento']
		facturaSiat.cabecera.codigoMetodoPago = invoiceData['codigo_metodo_pago']
		facturaSiat.cabecera.numeroTarjeta = invoiceData['numero_tarjeta']
		facturaSiat.cabecera.montoTotal = invoiceData['total']
		facturaSiat.cabecera.montoTotalSujetoIva = round((facturaSiat.cabecera.montoTotal - float(invoiceData['monto_giftcard'])), 2)  # invoiceData['total_tax']
		facturaSiat.cabecera.codigoMoneda = invoiceData['codigo_moneda']
		facturaSiat.cabecera.tipoCambio = invoiceData['tipo_cambio']
		facturaSiat.cabecera.montoTotalMoneda = round((facturaSiat.cabecera.montoTotal * facturaSiat.cabecera.tipoCambio), 2)
		facturaSiat.cabecera.montoGiftCard = float(invoiceData['monto_giftcard']) if float(invoiceData[
																				  'monto_giftcard']) > 0 else None
		facturaSiat.cabecera.descuentoAdicional = invoiceData['discount']
		facturaSiat.cabecera.codigoExcepcion = invoiceData['data']['excepcion'] if invoiceData['data'][
																					   'excepcion'] == 1 else None
		facturaSiat.cabecera.cafc = None
		facturaSiat.cabecera.usuario = None

		return facturaSiat

	def invoiceToSiatInvoice(self, invoice: Invoice):
		#MODIFY - Load Config of a branch
		config = self.getConfig(invoice.codigo_sucursal)
		#******************************************
		siatInvoice = SiatFactory.construirFactura(
			invoice.codigo_documento_sector,
			config.get('modalidad')
		)
		cufd = request.env['siat.cufd'].getByCode(invoice.cufd)
		if not cufd:
			raise Exception('No se puede contruir la factura SIAT, el CUFD de la factura no existe')

		current_user = request.env['res.users'].browse(request.env.uid)
		siatInvoice.cabecera.usuario				= current_user.login
		siatInvoice.cabecera.direccion				= cufd.direccion
		siatInvoice.cabecera.municipio				= config.get('ciudad')
		siatInvoice.cabecera.telefono				= config.get('telefono')
		siatInvoice.cabecera.nitEmisor				= invoice.nit_emisor
		siatInvoice.cabecera.razonSocialEmisor		= config.get('razonSocial')
		siatInvoice.cabecera.numeroFactura			= invoice.invoice_number
		siatInvoice.cabecera.fechaEmision			= siat_functions.sb_siat_format_datetime(invoice.invoice_datetime, None)
		siatInvoice.cabecera.cufd 					= invoice.cufd
		siatInvoice.cabecera.cuf 					= invoice.cuf
		siatInvoice.cabecera.montoTotal 			= invoice.total
		siatInvoice.cabecera.leyenda				= invoice.leyenda
		siatInvoice.cabecera.cafc					= None if not invoice.cafc else invoice.cafc
		siatInvoice.cabecera.codigoCliente 			= invoice.customer_id
		siatInvoice.cabecera.nombreRazonSocial 		= invoice.customer_name
		siatInvoice.cabecera.numeroDocumento		= invoice.nit_ruc_nif
		siatInvoice.cabecera.complemento			= None if not invoice.complemento else invoice.complemento
		siatInvoice.cabecera.codigoDocumentoSector 	= invoice.codigo_documento_sector
		siatInvoice.cabecera.codigoMetodoPago		= invoice.codigo_metodo_pago
		siatInvoice.cabecera.codigoMoneda			= invoice.codigo_moneda
		siatInvoice.cabecera.codigoSucursal			= invoice.codigo_sucursal
		siatInvoice.cabecera.codigoPuntoVenta		= invoice.punto_venta
		siatInvoice.cabecera.codigoTipoDocumentoIdentidad	= invoice.tipo_documento_identidad
		siatInvoice.cabecera.montoGiftCard					= invoice.monto_giftcard
		siatInvoice.cabecera.tipoCambio				= invoice.tipo_cambio
		siatInvoice.cabecera.descuentoAdicional		= invoice.discount
		siatInvoice.cabecera.montoTotal				= invoice.total
		siatInvoice.cabecera.montoTotalMoneda		= invoice.total * invoice.tipo_cambio
		siatInvoice.cabecera.montoTotalSujetoIva	= round((invoice.total - invoice.monto_giftcard), 2)
		siatInvoice.cabecera.numeroTarjeta			= None if not invoice.numero_tarjeta else invoice.numero_tarjeta
		siatInvoice.cabecera.codigoExcepcion		= invoice.get_data('excepcion')

		for item in invoice.items:
			siatDetalle = siatInvoice.instanceDetail()
			siatDetalle.descripcion 		= item.product_name
			siatDetalle.montoDescuento 		= item.discount
			siatDetalle.precioUnitario 		= item.price
			siatDetalle.subTotal			= item.total
			siatDetalle.unidadMedida		= item.unidad_medida
			siatDetalle.codigoProducto 		= item.product_code
			siatDetalle.actividadEconomica	= item.codigo_actividad
			siatDetalle.codigoProductoSin	= item.codigo_producto_sin
			siatDetalle.cantidad			= item.quantity

			siatInvoice.detalle.append( siatDetalle )

		return siatInvoice

	def create(self, invoiceData: dict):
		#MODIFY - Verify if invoice is POS or Siat (Set Discount and Nit/Ci/Complement)
		#**********************************************
		#MODIFY - Validate Decimals
		self.verify_decimals(invoiceData)
		#*******************************
		#MODIFY - Validate NIT minor sales of the day 
		self.verify_nit_99003(invoiceData)
		#*******************************
		current_user = request.env['res.users'].browse(request.env.uid)
		user_tz = request.env.user.tz or 'America/La_Paz' # pytz.timezone('America/La_Paz') #pytz.utc
		print('USER TIMEZONE', user_tz)
		invoiceData['company_id'] = request.env.company.id
		sucursal 	= invoiceData['codigo_sucursal']
		puntoventa 	= invoiceData['punto_venta']
		#MODIFY - Load Config With Branch
		config 		= self.getConfig(sucursal)
		#**********************************
		customer 	= request.env['res.partner'].browse(invoiceData['customer_id'])
		cuis 		= self.serviceSync.sync_cuis(sucursal, puntoventa)
		cufd 		= self.serviceSync.sync_cufd(sucursal, puntoventa)
		activeEvent = self.serviceEvents.eventoActivo(sucursal, puntoventa)
		facturaSiat = self.requestDataToSiatInvoice(invoiceData, config)
		facturaSiat.cabecera.usuario = current_user.login
		facturaSiat.cabecera.cufd = cufd.codigo
		facturaSiat.cabecera.direccion = cufd.direccion
		facturaSiat.cabecera.fechaEmision = siat_functions.sb_siat_format_datetime(datetime.now(),
																				   pytz.timezone(user_tz))
		facturaSiat.cabecera.codigoCliente = customer.id
		invoice_dict = None

		if activeEvent is not None:
			#MODIFY - Only for purchase sale - documentary sector
			if activeEvent.evento_id in [5,6,7]:
				if (config['cafc']):
					#MODIFY - Load Cafc
					facturaSiat.cabecera.cafc = json.loads(config['cafc'])['compra_venta']['cafc']
					#******************************************************
					#MODIFY - Load invoice_date_time input
					facturaSiat.cabecera.fechaEmision = invoiceData['invoice_date_time']
					#******************************************************
					#MODIFY - Update cufd event
					facturaSiat.cabecera.cufd = activeEvent.cufd_evento
					#******************************************************
				else: 
					raise Exception('El CAFC del evento no existe')
			#******************************************************
			if invoiceData['tipo_documento_identidad'] == 5:
				facturaSiat.cabecera.codigoExcepcion = 1
			cufd_evento = activeEvent.get_cufd_evento()
			if not cufd_evento:
				raise Exception('El CUFD del evento no existe')

			facturaSiat.buildCuf(
				config['modalidad'],
				siat_constants.TIPO_EMISION_OFFLINE,
				siat_constants.TIPO_FACTURA_CREDITO_FISCAL,
				cufd_evento.codigo_control
			)
			facturaSiat.validate()
			invoice_dict = self.siatInvoiceToInvoice(facturaSiat)
			invoice_dict['tipo_emision'] = siat_constants.TIPO_EMISION_OFFLINE
			invoice_dict['control_code'] = cufd_evento.codigo_control
			invoice_dict['evento_id'] = activeEvent.id
		else:
			if invoiceData['tipo_documento_identidad'] == 5 and invoiceData['data'].get('excepcion', 0) != 1:
				service_codes = self.serviceSync.getSiatServiceCodes()
				service_codes.cuis = cuis['codigo']
				res = service_codes.verificarNit(invoiceData['nit_ruc_nif'], sucursal, puntoventa)
				print(res)
				if res['mensajesList'][0]['codigo'] == 994 or res['mensajesList'][0]['codigo'] == 987:
					raise SiatExceptionInvalidNit(res, 'El NIT "{0}" no es valido'.format(invoiceData['nit_ruc_nif']))

			serviceFacturacion = SiatFactory.obtenerServicioFacturacion(config, cuis['codigo'], cufd.codigo, cufd.codigo_control)
			print(facturaSiat.cabecera.montoTotal, 'FACTURA SIAT - ***********************************')
			siat_response = serviceFacturacion.recepcionFactura(facturaSiat, siat_constants.TIPO_EMISION_ONLINE, siat_constants.TIPO_FACTURA_CREDITO_FISCAL)
			print(siat_response, 'SIAT RESPONSE *****************************************')
			if siat_response is None:
				raise Exception('SIAT ERROR: Respuesta de impuestos invalida')
			if siat_response['codigoEstado'] != 908:
				print( serviceFacturacion.buildInvoiceXml(facturaSiat) )
				raise Exception( siat_functions.sb_siat_response_message(siat_response) )
		
			invoice_dict = self.siatInvoiceToInvoice(facturaSiat)
			invoice_dict['siat_id'] 		= siat_response['codigoRecepcion']
			invoice_dict['tipo_emision'] 	= siat_constants.TIPO_EMISION_ONLINE
			invoice_dict['control_code']	= cufd.codigo_control

		invoice_dict['customer_id'] = customer.id
		invoice_dict['tipo_factura_documento'] = siat_constants.TIPO_FACTURA_CREDITO_FISCAL
		invoice_dict['ambiente'] = config['ambiente']
		invoice_dict['company_id'] = request.env.company.id
	
		invoice = request.env['siat.invoice'].create(invoice_dict)

		# for detalle in facturaSiat.detalle:
		for request_item in invoiceData['items']:
			# invoice_item = self.siatDetailToInvoiceDetail(detalle)
			#invoice_item.invoice_id = invoice.id
			#invoice_item.product_id = 0
			invoice_item = {
				'invoice_id': invoice.id,
				'product_id': request_item['product_id'],
				'product_code': request_item['product_code'],
				'codigo_producto_sin': request_item['codigo_producto_sin'],
				'unidad_medida': request_item['unidad_medida'],
				'product_name': request_item['product_name'],
				'codigo_actividad': request_item['codigo_actividad'],
				'numero_seria': request_item.get('numero_serie', ''),
				'numero_imei': request_item['numero_imei'],
				'nandina': request_item.get('nandina', ''),
				'price': request_item['price'],
				'quantity': request_item['quantity'],
				'subtotal': round(request_item['price'] * request_item['quantity'], 2),
				'discount': request_item['discount'],
				'total': round(((request_item['price'] * request_item['quantity']) - request_item['discount']), 2),
			}
			request.env['siat.invoiceitem'].create(invoice_item)

		# send customer email
		self.send_customer_email(invoice)
		# self.send_customer_email_with_thread(invoice)
		return invoice

	def send_customer_email_with_thread(self, invoice: Invoice):
		import threading
		mail_thread = threading.Thread(target=self.send_customer_email, args=(invoice,))
		mail_thread.start()
		mail_thread.join()

	def send_customer_email(self, invoice: Invoice):
		'''
		ir_model_data = request.env['ir.model.data']
		template_id = ir_model_data.get_object_reference('siat', 'siat_invoice_email_template')
		compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
		'''

		cuis = self.serviceSync.sync_cuis(invoice.codigo_sucursal, invoice.punto_venta)
		cufd = self.serviceSync.sync_cufd(invoice.codigo_sucursal, invoice.punto_venta)
		service = SiatFactory.obtenerServicioFacturacion(
			self.getConfig(invoice.codigo_sucursal),
			cuis['codigo'],
			cufd.codigo,
			cufd.codigo_control
		)
		customer = invoice.get_customer()
		siat_invoice = self.invoiceToSiatInvoice(invoice)
		xml = service.buildInvoiceXml(siat_invoice)
		#print('XML', xml.decode('utf8'))

		ctx = {
			'email_from': 'facturacion@1bytebo.net',
			'email_to': customer.email,
		}

		# email_template = request.env['mail.template'].browse('siat_invoice_email_template')
		# email_template = request.env['mail.template'].search([('')])
		email_template = request.env.ref('siat.siat_invoice_email_template')
		# print('EMAIL TEMPLATE', email_template)
		print('EMAILTO: ', customer.email)
		# '''
		SiatMailTemplate.append_attachments.append(
			(
				'FACTURA_{0}_{1}.xml'.format(invoice.company_id.name, invoice.invoice_number),
				base64.b64encode(xml)
			)
		)
		# '''
		email_template[0].send_mail(invoice.id, force_send=True, email_values=ctx)
		SiatMailTemplate.append_attachments = []

	def void(self, id: int, motivo_anulacion: int):
		invoices = request.env['siat.invoice'].browse(id)
		if len(invoices) <= 0:
			raise Exception('La factura no existe')
		invoice = invoices[0]

		config = self.getConfig(invoice.codigo_sucursal)
		cuis = self.serviceSync.sync_cuis(invoice.codigo_sucursal, invoice.punto_venta)
		cufd = self.serviceSync.sync_cufd(invoice.codigo_sucursal, invoice.punto_venta)
		service = SiatFactory.obtenerServicioFacturacion(
			config,
			cuis['codigo'],
			cufd.codigo,
			cufd.codigo_control
		)
		service.debug = True
		res = service.anulacionFactura(
			motivo_anulacion,
			invoice.cuf,
			invoice.codigo_sucursal,
			invoice.punto_venta,
			invoice.tipo_factura_documento,
			# invoice.tipo_emision,
			siat_constants.TIPO_EMISION_ONLINE,
			invoice.codigo_documento_sector
		)

		# if (res['codigoEstado'] in [905, 906]) is False:
		if res['codigoEstado'] != 905:
			print('SIAT ANULAR ERROR', res)
			raise Exception('No se puedo anular la factura')

		print('SIAT VOID RES', res)
		void_datetime = siat_functions.sb_siat_format_datetime(datetime.now())
		invoice.write({
			'status': Invoice.STATUS_VOID,
			'void_datetime': datetime.strptime(void_datetime, siat_constants.DATETIME_FORMAT),
		})
		self.send_customer_void_email(invoice)

		return invoice
	
	#MODIFY - Method renew
	def renovar(self, invoice: Invoice):
		config = self.getConfig(invoice.codigo_sucursal)
		cuis = self.serviceSync.sync_cuis(invoice.codigo_sucursal, invoice.punto_venta)
		cufd = self.serviceSync.sync_cufd(invoice.codigo_sucursal, invoice.punto_venta)
		service = SiatFactory.obtenerServicioFacturacion(
			config,
			cuis['codigo'],
			cufd.codigo,
			cufd.codigo_control
		)
		service.debug = True
		res = service.renovacionFactura(
			0,
			invoice.cuf,
			invoice.codigo_sucursal,
			invoice.punto_venta,
			invoice.tipo_factura_documento,
			# invoice.tipo_emision,
			siat_constants.TIPO_EMISION_ONLINE,
			invoice.codigo_documento_sector
		)

		# if (res['codigoEstado'] in [905, 906]) is False:
		if res['codigoEstado'] != 907:
			print('SIAT ANULAR ERROR', res)
			raise Exception('No se puedo anular la factura')

		print('SIAT RENEW RES', res)

		void_datetime = siat_functions.sb_siat_format_datetime(datetime.now())
		invoice.write({
			'status': Invoice.STATUS_RENOVATED,
			'void_datetime': datetime.strptime(void_datetime, siat_constants.DATETIME_FORMAT),
		})

		self.send_customer_void_email(invoice)

		return invoice
	#*********************************************************************************

	def send_customer_void_email(self, invoice: Invoice):
		data = {}
		email_template = request.env.ref('siat.siat_invoice_void_email_template')
		email_template[0].send_mail(invoice.id, force_send=True, email_values=data)

	def verify_decimals (self, invoice):
		# Convertir el valor a una cadena de texto y contar los dígitos después del punto decimal
		number: any
		if '.' in str(invoice['discount']):
			number = str(invoice['discount']).split('.')[1]
			if len(number) > 2:
				raise Exception('El Descuento general debe contener como máximo 2 decimales')
		for request_item in invoice['items']:
			if '.' in str(request_item['price']):
				number = str(request_item['price']).split('.')[1]
				if len(number) > 2:
					raise Exception('El Precio del producto ' + request_item['product_name']  + ' debe contener como máximo 2 decimales')
			if '.' in str(request_item['discount']):
				number = str(request_item['discount']).split('.')[1]
				if len(number) > 2:
					raise Exception('El Descuento del producto ' + request_item['product_name']  + ' debe contener como máximo 2 decimales')()
				
	def verify_nit_99003 (self, invoice):
		if(invoice['nit_ruc_nif'] == 99003):
			for request_item in invoice['items']:
				if ((request_item['price'] * request_item['quantity'] - request_item['discount']) > 5):
					raise Exception('El subtotal del producto ' + request_item['product_name']  + ' debe tener un valor máximo de 5 Bs (Ventas Menores del día)')

