# -*- coding: utf-8 -*-
import logging
import json
import traceback

from odoo import http, _
from odoo.http import request, Controller
from odoo.osv.expression import AND
from odoo.tools import format_amount
# from odoo.addons.account.controllers.portal import PortalAccount

from ..libsiat import constants as siat_constants
from ..libsiat.classes.siat_exception import SiatException
from ..services.service_siat_sync import ServiceSiatSync
from ..services.service_siat_events import ServiceSiatEvents
from ..resources.resource_event import ResourceEvent
from .siat_controller import SiatController

_logger = logging.getLogger(__name__)


class SiatSyncController(Controller, SiatController):

	@http.route(['/siat/eventos/activo', '/siat/eventos/activo/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'], type='http', auth='user', methods=['GET'], csrf=False)
	def activo(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int( params.get('puntoventa', 0) )
		service = ServiceSiatEvents()
		event = service.eventoActivo(sucursal, puntoventa)
		
		return request.make_json_response({
			'status': 'ok',
			'code': 200,
			'data': event.read()[0] if event is not None else None
		})

	@http.route(['/siat/eventos'], type='http', auth='user', methods=['POST', 'PUT'], csrf=False)
	def create(self, **params):
		self._check_session()
		data = json.loads(request.httprequest.data)
		
		try:
			service = ServiceSiatEvents()
			event = service.create(data)
			
			return request.make_json_response({
				'status': 'ok',
				'code': 200,
				'data': event.read()[0]
			})
			
		except Exception as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error', 
				'code': code, 
				'data': None,
				'error': str(e)
			}, status=code)
		
	@http.route(['/siat/eventos',
		'/siat/eventos/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>', 
		'/siat/eventos/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>/page/<int:page>'], type='http', auth='user', methods=['GET'])
	def readAll(self, **params):
		self._check_session()
		sucursal = params.get('sucursal', 0)
		puntoventa = params.get('puntoventa', 0)
		page = params.get('page', 1)
		events = request.env['siat.event'].search([('sucursal_id', '=', sucursal), ('puntoventa_id', '=', puntoventa)], order='id desc', limit=25)
		items = []
		for event in events:
			resource = ResourceEvent(event)
			items.append( resource.dict() )
			
		return request.make_json_response({
			'status': 'ok',
			'code': 200,
			'data': items
		})
	
	@http.route(['/siat/eventos/<int:id>/anular'], type='http', auth='user', methods=['GET'])
	def void(self, **params):
		self._check_session()
		try:
			id = params.get('id', 0)
			if id <= 0:
				raise Exception('El identificador del evento is invalido')
				
			service = ServiceSiatEvents()
			event = service.void(id)
			
			return request.make_json_response({
				'status': 'ok',
				'code': 200,
				'data': event.read()[0]
			})
			
		except Exception as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error', 
				'code': code, 
				'data': None,
				'error': str(e)
			}, status=code)

	@http.route(['/siat/eventos/<int:id>/stats'], type='http', auth='user', methods=['GET'])
	def stats(self, **params):
		self._check_session()
		return request.make_json_response({
			'status': 'ok',
			'code': 200,
			'data': {}
		})

	@http.route(['/siat/eventos/<int:id>/cerrar'], type='http', auth='user', methods=['GET'])
	def close(self, **params):
		self._check_session()
		try:
			id = params.get('id', 0)
			if id <= 0:
				raise Exception('Identificador de evento invalido')

			service = ServiceSiatEvents()
			event = service.close(id)

			return request.make_json_response({
				'status': 'ok',
				'data': event[0].read()
			})

		except Exception as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error',
				'code': code,
				'data': None,
				'error': str(e)
			}, status=code)

	@http.route(['/siat/eventos/<int:id>/validar-recepcion'], type='http', auth='user', methods=['GET'])
	def verify(self, **params):
		self._check_session()
		try:
			id = params.get('id', 0)
			if id <= 0:
				raise Exception('Identificador de evento invalido')

			service = ServiceSiatEvents()
			event = service.verify_event_reception(id)

			return request.make_json_response({
				'status': 'ok',
				'data': event[0].read()
			})
		except Exception as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error',
				'code': code,
				'data': None,
				'error': str(e)
			}, status=code)