import pytz
from datetime import datetime, timedelta

from odoo import http, _
from odoo.http import request, Controller

from .service_siat import ServiceSiat
from .service_siat_sync import ServiceSiatSync
from ..models.invoice import Invoice
from ..libsiat.classes.siat_factory import SiatFactory
from ..libsiat.services.service_operaciones import ServiceOperaciones
from ..libsiat import functions as siat_functions
from ..libsiat import constants as siat_constants
from ..models.branch import Branch


class ServiceSiatOperations(ServiceSiatSync):
	
	def __init__(self):
		super().__init__()

		self.serviceOperaciones = ServiceOperaciones()
		self.serviceOperaciones.setConfig(self.getConfig())

		
	def nitValido(self, nit):
		
		res = self.serviceOperaciones.verificarNit(nit)
		print(res)
		
	def registrarEvento(self, data: dict):
		print(data)
		cuis = self.sync_cuis(data['sucursal'], data['puntoventa'])
		cufd = self.sync_cufd(data['sucursal'], data['puntoventa'])
		self.serviceOperaciones.cuis = cuis['codigo']
		self.serviceOperaciones.cufd = cufd.codigo
		self.serviceOperaciones.debug = True
		res = self.serviceOperaciones.registroEventoSignificativo(
			data['evento_id'],
			data['descripcion'],
			data['cufd_evento'],
			data['fecha_inicio'],
			data['fecha_fin'],
			data['sucursal'],
			data['puntoventa']
		)
		print(res)
		
		return res

	def consulta_puntos_venta(self, sucursal=0):
		cuis = self.sync_cuis(sucursal)
		self.serviceOperaciones.cuis = cuis['codigo']
		res = self.serviceOperaciones.consultaPuntoVenta(sucursal)

		return res

	def registrar_puntoventa(self, sucursal_id: int, codigo_sucursal: int, tipo: int, nombre: str, descripcion: str):
		#sucursal = request.env['siat.event'].browse(sucursal_id)
		#if sucursal is None or len(sucursal) <= 0:
		#	raise Exception('Sucursal inexistente')

		cuis = self.sync_cuis(codigo_sucursal)
		self.serviceOperaciones.cuis = cuis['codigo']
		res = self.serviceOperaciones.registroPuntoVenta(codigo_sucursal, tipo, nombre, descripcion)
		print('RES', res)

		pos = request.env['siat.pos'].create({
			'sucursal_id': sucursal_id,
			'codigo': res['codigoPuntoVenta'],
			'codigo_sucursal': codigo_sucursal,
			'tipo_id': tipo,
			'tipo_descripcion': descripcion,
			'nombre': nombre,
			'descripcion': '',
			'direccion': '',
			'ciudad': '',
			'telefono': '',
		})
		return pos

	def borrar_puntoventa(self, pid: int):
		poss = request.env['siat.pos'].browse(pid)
		if len(poss) <= 0:
			raise Exception('El punto de venta no existe, no se puede borrar')
		pos = poss[0]

		if pos.codigo <= 0:
			pos.unlink()
			return True
		cuis = self.sync_cuis(pos.codigo_sucursal)
		self.serviceOperaciones.cuis = cuis['codigo']
		res = self.serviceOperaciones.cierrePuntoVenta(pos.codigo_sucursal, pos.codigo)
		if res['transaccion'] is False:
			print('ERROR', res)
			raise Exception('Ocurrio un error al borrar el punto de venta')

		pos.unlink()
		return res
		
