from .service_siat import ServiceSiat
from datetime import datetime

from .. import functions

class ServiceOperaciones(ServiceSiat):
	
	def __init__(self):
		super().__init__()
		self.wsdl = 'https://pilotosiatservicios.impuestos.gob.bo/v2/FacturacionOperaciones?wsdl'
		
	def _buildData(self, sucursal, puntoventa, fecha: str):
		
		return {
			'codigoAmbiente': self.ambiente,
			'codigoPuntoVenta': puntoventa,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': self.sucursal,
			'cufd': self.cufd,
			'nit': self.nit,
			'fechaEvento': fecha
		}
		
	def registroEventoSignificativo(self, codigoEvento: int, descripcion, cufdEvento, fechaInicio: datetime, fechaFin: datetime, sucursal, puntoventa):
		
		data = [{
			'codigoAmbiente': self.ambiente,
			'codigoMotivoEvento': codigoEvento,
			'codigoPuntoVenta': puntoventa,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': sucursal,
			'cufd': self.cufd,
			'cufdEvento': cufdEvento,
			'cuis': self.cuis,
			'descripcion': descripcion,
			'fechaHoraInicioEvento': functions.sb_siat_format_datetime(fechaInicio, None),
			'fechaHoraFinEvento': functions.sb_siat_format_datetime(fechaFin, None),
			'nit': self.nit,
		}]
		self.debugData(data)
		res = self.callAction('registroEventoSignificativo', data)
		
		return res
	
	def consultaEventoSignificativo(self, sucursal, puntoventa, fecha: datetime):
		data = self._buildData(sucursal, puntoventa, datetime.strftime(fecha, '%Y-%m-%d'))
		
		res = self.callAction('consultaEventoSignificativo', [data])
		return res
		
	'''
	Registra un nuevo punto de venta
	'''
	def registroPuntoVenta(self, sucursal: int, tipoPuntoVenta: int, nombrePuntoVenta, descripcion):
		data = [{
			'codigoAmbiente': self.ambiente,
			'codigoModalidad': self.modalidad,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': sucursal,
			'codigoTipoPuntoVenta': tipoPuntoVenta,
			'cuis': self.cuis,
			'descripcion': descripcion,
			'nit': self.nit,
			'nombrePuntoVenta': nombrePuntoVenta,
		}]
		
		res = self.callAction('registroPuntoVenta', data)
		
		return res
		
	def consultaPuntoVenta(self, sucursal: int):
		data = [{
			'codigoAmbiente': self.ambiente,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': sucursal,
			'cuis': self.cuis,
			'nit': self.nit,
		}]
			
		res = self.callAction('consultaPuntoVenta', data)
		
		return res
		
	def cierrePuntoVenta(self, sucursal: int, puntoventa: int):
		data = [{
			'codigoAmbiente': self.ambiente,
			'codigoPuntoVenta': puntoventa,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': sucursal,
			'cuis': self.cuis,
			'nit': self.nit,
		}]
	
		res = self.callAction('cierrePuntoVenta', data)
		
		return res
		
	def cierreOperacionesSistema(self, sucursal: int, puntoventa: int):
		data = [{
			'codigoAmbiente': self.ambiente,
			'codigoModalidad': self.modalidad,
			'codigoPuntoVenta': puntoventa,
			'codigoSistema': self.codigoSistema,
			'codigoSucursal': sucursal,
			'cuis': self.cuis,
			'nit': self.nit,
		}]
		
		res = self.callAction('cierreOperacionesSistema', data)
		
		return res
		
	
		
