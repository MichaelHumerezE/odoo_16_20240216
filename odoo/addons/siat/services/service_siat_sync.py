# -*- coding: utf-8 -*-
import logging
import datetime
import os
import time
import json
import random

from odoo.http import request

from ..libsiat import constants as siat_constants
from ..libsiat import functions as siat_functions
from ..libsiat.classes.siat_exception import SiatException
from ..libsiat.services.service_codigos import ServiceCodigos
from ..libsiat.services.service_sincronizacion import ServiceSincronizacion
from .service_siat import ServiceSiat

_logger = logging.getLogger(__name__)


class ServiceSiatSync(ServiceSiat):

	def __init__(self):
		self.check_session()
		self.DATA_DIR = os.path.dirname(os.path.dirname(__file__)) + '/siat_data'
		if os.path.isdir(self.DATA_DIR) == False:
			os.mkdir( self.DATA_DIR )
			
		print('SIAT DATA DIR', self.DATA_DIR)
		cfg = self.getConfig(0)
		# print('SYNC CONFIG', cfg)
		self._serviceCodes = ServiceCodigos()
		self._serviceCodes.setConfig(cfg)
		
		self._serviceSync = ServiceSincronizacion()
		self._serviceSync.setConfig(cfg)
	
	def getSiatServiceCodes(self):
		
		return self._serviceCodes
	
	def file_needs_sync(self, filename):
		if os.path.isfile(filename) is False:
			return True
		
		HOUR_SECONDS = 3600
		DAY_SECONDS = HOUR_SECONDS * 24
		
		modification_time = os.path.getmtime(filename)
		modification_datetime = datetime.datetime.fromtimestamp(modification_time)
		unix_modification_time = int(time.mktime(modification_datetime.timetuple()))
		unix_current_time = int(time.mktime(datetime.datetime.now().timetuple()))
		
		time_diff = unix_current_time - unix_modification_time
		
		if time_diff > DAY_SECONDS:
			return True
			
		return False
	
	def write_json_file(self, dicData, filename):
		json_str = json.dumps(dicData, default=str)
		with open(filename, 'w', encoding='utf-8') as f_out:
			f_out.write( json_str )
			
	def sync_cuis(self, sucursal=0, puntoventa=0):
		filename = '{0}/cuis-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
		
		cuis = self._serviceCodes.getCuis(sucursal, puntoventa)
		if cuis['transaccion'] == False and cuis['codigo'] is None:
			raise SiatException(cuis)
		
		self.write_json_file(cuis, filename)
		
		return cuis

	def sync_cufd(self, sucursal=0, puntoventa=0, renew=0):
		
		latest = request.env['siat.cufd'].getLatest(request.env.company.id, sucursal, puntoventa)
		
		if renew == 0 and latest is not None and len(latest) > 0:
			# _logger.info(latest.read())
			if latest.isExpired() is False:
				return latest
		
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceCodes.cuis = cuis['codigo']
		
		cufd = self._serviceCodes.getCufd(sucursal, puntoventa)
	
		if cufd['transaccion'] == False and cufd['codigo'] is None:
			raise SiatException(cufd)
			
		# newCufd = Cufd()
		# fecha_vigencia = datetime.datetime.strptime(cufd['fechaVigencia'], '%Y-%m-%d %H:%M:%S').date()
		fecha_vigencia = cufd['fechaVigencia'].strftime('%Y-%m-%d %H:%M:%S')
		_logger.info(fecha_vigencia);
		newCufd = request.env['siat.cufd'].create({
			'codigo': cufd['codigo'],
			'codigo_control': cufd['codigoControl'],
			'direccion': cufd['direccion'],
			'sucursal_id': sucursal,
			'puntoventa_id': puntoventa,
			'fecha_creacion': siat_functions.sb_siat_localize_datetime(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
			'fecha_vigencia': fecha_vigencia,
			'company_id': request.env.company.id,
		})
		# _logger.info(type(newCufd))
		
		return newCufd

	def sync_unidades_medida(self, sucursal=0, puntoventa=0):
		
		filename = '{0}/unidades-medida-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) is False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaUnidadMedida(sucursal, puntoventa)
		if res is None:
			return None
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)

		return data

	def sync_tipos_moneda(self, sucursal=0, puntoventa=0):
		filename = '{0}/tipos-moneda-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoMoneda(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
	
	def sync_documentos_identidad(self, sucursal=0, puntoventa=0):
		filename = '{0}/documentos-identidad-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoDocumentoIdentidad(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_productos_servicios(self, sucursal=0, puntoventa=0):
		filename = '{0}/productos-servicios-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) is False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarListaProductosServicios(sucursal, puntoventa)
		if res is None:
			return None
		data = {'RespuestaListaProductos': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_metodos_pago(self, sucursal=0, puntoventa=0):
		filename = '{0}/metodos-pago-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoMetodoPago(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_actividades(self, sucursal=0, puntoventa=0):
		filename = '{0}/actividades-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarActividades(sucursal, puntoventa)
		if res is None:
			return None
		data = {'RespuestaListaActividades': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_actividad_documento_sector(self, sucursal=0, puntoventa=0):
		filename = '{0}/actividades-doc-sector-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarListaActividadesDocumentoSector(sucursal, puntoventa)
		
		data = {'RespuestaListaActividadesDocumentoSector': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_leyendas(self, sucursal=0, puntoventa=0):
		filename = '{0}/leyendas-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarListaLeyendasFactura(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricasLeyendas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_eventos(self, sucursal=0, puntoventa=0):
		filename = '{0}/eventos-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaEventosSignificativos(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_motivos_anulacion(self, sucursal=0, puntoventa=0):
		filename = '{0}/motivos-anulacion-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaMotivoAnulacion(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_documentos_sector(self, sucursal=0, puntoventa=0):
		filename = '{0}/documentos-sector-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoDocumentoSector(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_tipos_emision(self, sucursal=0, puntoventa=0):
		filename = '{0}/tipos-emision-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoEmision(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_tipos_puntoventa(self, sucursal=0, puntoventa=0):
		filename = '{0}/tipos-puntoventa-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoPuntoVenta(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_tipos_factura(self, sucursal=0, puntoventa=0):
		filename = '{0}/tipos-factura-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTiposFactura(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def sync_tipos_habitacion(self, sucursal=0, puntoventa=0):
		filename = '{0}/tipos-habitacion-{1}-{2}.json'.format(self.DATA_DIR, sucursal, puntoventa)
		
		if self.file_needs_sync( filename ) == False:
			return json.loads( self.file_get_contents( filename ) )
			
		cuis = self.sync_cuis(sucursal, puntoventa)
		self._serviceSync.cuis = cuis['codigo']
		res = self._serviceSync.sincronizarParametricaTipoHabitacion(sucursal, puntoventa)
		
		data = {'RespuestaListaParametricas': res}
		self.write_json_file(data, filename)
		
		return data
		
	def leyenda_aleatoria(self, codigo_actividad):
		data = self.sync_leyendas()
		total_items = len( data['RespuestaListaParametricasLeyendas']['listaLeyendas'] )
		index = int( random.randint(0, total_items - 1) )
		
		# print(data['RespuestaListaParametricasLeyendas']['listaLeyendas'], 'index: ', index)
		leyendas = []
		for item in data['RespuestaListaParametricasLeyendas']['listaLeyendas']:
			if item['codigoActividad'] == codigo_actividad:
				leyendas.append( item )
				
		total_items = len( leyendas )
		if total_items <= 0:
			
			return data['RespuestaListaParametricasLeyendas']['listaLeyendas'][index]['descripcionLeyenda']
			
		index = int( random.randint(0, total_items - 1) )
		
		return leyendas[index]['descripcionLeyenda']
		
	def buscar_evento(self, codigo_evento):
		eventos = self.sync_eventos()
		
		evento = None
		for item in eventos['RespuestaListaParametricas']['listaCodigos']:
			if item['codigoClasificador'] == codigo_evento:
				evento = item
				break
				
		return evento

	def buscar_unidad_medida(self, codigo_unidad_medida: int):
		unidades = self.sync_unidades_medida()
		unidad = None
		for item in unidades['RespuestaListaParametricas']['listaCodigos']:
			if item['codigoClasificador'] == codigo_unidad_medida:
				unidad = item
				break

		return unidad