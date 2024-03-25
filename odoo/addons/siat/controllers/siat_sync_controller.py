# -*- coding: utf-8 -*-
import logging
import traceback

from odoo import http, _
from odoo.http import request, Controller
from odoo.osv.expression import AND
from odoo.tools import format_amount
# from odoo.addons.account.controllers.portal import PortalAccount

from ..libsiat import constants as siat_constants
from ..libsiat.classes.siat_exception import SiatException
from ..libsiat.services.service_codigos import ServiceCodigos
from ..services.service_siat_sync import ServiceSiatSync
from .siat_controller import SiatController
_logger = logging.getLogger(__name__)


class SiatSyncController(Controller, SiatController):
		
	@http.route([
		'/siat/sync/cuis', 
		'/siat/sync/cuis/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>', 
		'/siat/sync/cuis/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>/renew/<int:renew>'], 
		type='http', auth='public', methods=['GET'])
	def sync_cuis(self, **params):
		self._check_session()
		# response.headers['Cache-Control'] = 'no-store'
		# _logger.info('CONNECTION SUCCESSFUL!!')
		#_logger.info(request.get_http_params())
		_logger.info(params)
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int( params.get('puntoventa', 0) )
		
		try:
			service  = ServiceSiatSync()
			cuis = service.sync_cuis(sucursal, puntoventa)
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': cuis})
		except SiatException as e:
			print('SIAT ERROR', e.getMessage())
			print('SIAT RESPONSE', e.response)
			return request.make_json_response({'status': 'ok', 'code': 500, 'data': None, 'error': e.getMessage()}, status=500)
		except Exception as e:
			print('GENERAL ERROR', e)
			print(traceback.print_exc())
			return request.make_json_response({'status': 'error', 'code': 500, 'data': None, 'error': str(e)}, status=500)
		
		# return request.make_response(data)
		
	@http.route([
			'/siat/sync/cufd', 
			'/siat/sync/cufd/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>',
			'/siat/sync/cufd/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>/renew/<int:renew>'
		],
		type='http', auth='user', methods=['GET'])
	def sync_cufd(self, **params):
		self._check_session()
		# response.headers['Cache-Control'] = 'no-store'
		# _logger.info('CONNECTION SUCCESSFUL!!')
		#_logger.info(request.get_http_params())
		_logger.info(params)
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int( params.get('puntoventa', 0) )
		renew = int( params.get('renew', 0) )
		
		try:
			service  = ServiceSiatSync()
			cufd = service.sync_cufd(sucursal, puntoventa, renew)
			
			return request.make_json_response({'status': 'ok', 'code': 200,
				'data': cufd.read()[0] if cufd is not None and len(cufd) > 0 else {}
			})
			
		except SiatException as e:
			print('SIAT ERROR', e.getMessage())
			print('SIAT RESPONSE', e.response)
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': None, 'error': e.getMessage()}, status=500)
		except Exception as e:
			print('GENERAL ERROR', e)
			# print(traceback.print_exc())
			return request.make_json_response({'status': 'error', 'code': 500, 'data': None, 'error': str(e)}, status=500)
		
	@http.route([
			'/siat/sync/puntosventa', 
			'/siat/sync/puntosventa/sucursal/<int:sucursal>',
		], 
		type='http', auth='public', methods=['GET'])
	def sync_puntosventa(self, **params):
		self._check_session()
		# response.headers['Cache-Control'] = 'no-store'
		# _logger.info('CONNECTION SUCCESSFUL!!')
		#_logger.info(request.get_http_params())
		# _logger.info(params)
		
		sucursal = int(params.get('sucursal', 0))
		limit = int(params.get('limit', 25))
		try:
			items = request.env['siat.pos'].search([('codigo_sucursal', '=', sucursal)], order='id desc', limit=limit)
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': items.read()})
		except SiatException as e:
			print('SIAT ERROR', e.getMessage())
			print('SIAT RESPONSE', e.response)
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': None, 'error': e.getMessage()}, status=500)
		except Exception as e:
			print('GENERAL ERROR', e)
			print(traceback.print_exc())
			return request.make_json_response({'status': 'error', 'code': 500, 'data': None, 'error': str(e)}, status=500)
	
	@http.route(['/siat/sync/unidades_medida'], auth='user', methods=['GET'])
	def sync_unidades_medida(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_unidades_medida(sucursal, puntoventa)

		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/unidades_medida','/siat/sync/unidades_medida/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_unidades_medida_piloto(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_unidades_medida(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_moneda','/siat/sync/tipos_moneda/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_tipos_moneda(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_moneda(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/documentos_identidad'], auth='user', methods=['GET'])
	def sync_documentos_identidad(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_documentos_identidad(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/documentos_identidad','/siat/sync/documentos_identidad/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_documentos_identidad(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_documentos_identidad(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/productos_servicios','/siat/sync/productos_servicios/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_productos_servicios(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_productos_servicios(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/metodos_pago'], auth='user', methods=['GET'])
	def sync_metodos_pago(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_metodos_pago(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/metodos_pago','/siat/sync/metodos_pago/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_metodos_pago_piloto(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_metodos_pago(sucursal, puntoventa)
		listaCodigos = res['RespuestaListaParametricas']['listaCodigos']
		print(listaCodigos)
		for item in sorted(listaCodigos, key=lambda x: x["codigoClasificador"]):
            #MODIFY - Verify Method Payment
			mp = request.env['pos.payment.method'].search([('code', '=', item['codigoClasificador'])], limit=1)
			if not mp:
				request.env['pos.payment.method'].create({
                    'name': item['descripcion'],
                    'code': item['codigoClasificador'],
					'is_cash_count': True,
					'journal_id': 7,
					'create_uid': 1,
					'write_uid': 1,
					'split_transactions': True
                })
            #**************************************************************
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/actividades','/siat/sync/actividades/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_actividades(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_actividades(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/actividades_doc_sector'], auth='user', methods=['GET'])
	def sync_actividades_doc_sector(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_actividad_documento_sector(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/actividades_doc_sector','/siat/sync/actividades_doc_sector/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_actividades_doc_sector_piloto(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_actividad_documento_sector(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/leyendas','/siat/sync/leyendas/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_leyendas(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_leyendas(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_habitacion','/siat/sync/tipos_habitacion/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_tipos_habitacion(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_habitacion(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/eventos','/siat/sync/eventos/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_eventos(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_eventos(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/motivos_anulacion'], auth='user', methods=['GET'])
	def sync_motivos_anulacion(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_motivos_anulacion(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/motivos_anulacion','/siat/sync/motivos_anulacion/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_motivos_anulacion_piloto(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_motivos_anulacion(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_documentos_sector','/siat/sync/tipos_documentos_sector/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_documentos_sector(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_documentos_sector(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_emision','/siat/sync/tipos_emision/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_emision(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_emision(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_puntoventa'], auth='user', methods=['GET'])
	def sync_tipos_puntoventa(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_puntoventa(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
	@http.route(['/siat/sync/tipos_puntoventa','/siat/sync/tipos_puntoventa/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_tipos_puntoventa_piloto(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_puntoventa(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
		
	@http.route(['/siat/sync/tipos_facturas','/siat/sync/tipos_facturas/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'],type='http', auth='user', methods=['GET'])
	def sync_tipos_facturas(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		service  = ServiceSiatSync()
		res = service.sync_tipos_factura(sucursal, puntoventa)
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': res})
	
