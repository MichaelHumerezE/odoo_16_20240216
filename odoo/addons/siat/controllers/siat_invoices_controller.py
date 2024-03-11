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
from ..libsiat.classes.siat_exception import SiatException, SiatExceptionInvalidNit
from ..services.service_invoices import ServiceInvoices
from ..resources.resource_invoice import ResourceInvoice
from .siat_controller import SiatController

_logger = logging.getLogger(__name__)


class SiatSyncController(Controller, SiatController):
	
	@http.route([
		'/siat/invoices', '/siat/invoices/page/<int:page>',
		'/siat/invoices/page/<int:page>/limit/<int:limit>'],
		type='http', auth='user', methods=['GET'], csrf=True
	)
	def readAll(self, **params):
		self._check_session()
		page = params.get('page', 1)
		limit = params.get('limit', 25)
		
		invoices = request.env['siat.invoice'].search([('company_id', '=', request.env.company.id)], order='id DESC', limit=limit)
		items = []
		for invoice in invoices:
			res = ResourceInvoice(invoice)
			items.append( res.dict() )
			
		return request.make_json_response({
			'status': 'ok', 
			'code': 200, 
			'length': 0,
			'data': items
		})
		
	@http.route(['/siat/invoices'], type='http', auth='user', methods=['POST', 'PUT'], csrf=False)
	def create(self, **params):
		self._check_session()
		data = json.loads(request.httprequest.data)
		service = ServiceInvoices()
		try:
			#MODIFY - DISCOUNT STR TO FLOAT
			data['discount'] = round(float(data['discount']), 2)
			#****************************************
			#MODIFY - TOTAL ROUNDED 2 DECIMAL
			data['total'] = round(data['total'], 2)
			#****************************************
			print(data)
			invoice = service.create(data)
			resource = ResourceInvoice(invoice)
			return request.make_json_response({
				'status': 'ok', 
				'code': 200, 
				'data': resource.dict()
			})
		except SiatExceptionInvalidNit as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error',
				'response': e.error_code,
				'code': code,
				'data': None,
				'error': e.getMessage()
			}, status=code)
		except Exception as e:
			print(traceback.print_exc())
			code = 500
			return request.make_json_response({
				'status': 'error', 
				'code': code, 
				'data': None,
				'error': str(e)
			}, status=code)
		
	@http.route(['/siat/invoices/<int:id>/void', '/siat/invoices/void/<int:id>'], type='http', auth='user', methods=['POST'], csrf=False)
	def void(self, **params):
		self._check_session()
		data = json.loads(request.httprequest.data)
		_id = data.get('invoice_id')
		_motivo = data.get('motivo_id')
		service = ServiceInvoices()
		invoice = service.void(_id, _motivo)
		resource = ResourceInvoice(invoice)

		return request.make_json_response({
			'status': 'ok',
			'code': 200,
			'data': resource.dict()
		})
	
	#MODIFY - Route api renewal invoice
	@http.route(['/siat/invoices/<int:id>/renovar'], type='http', auth='user', methods=['GET'])
	def renewal(self, **params):
		self._check_session()
		_id = params.get('id')
		print('+++++++++++++++++++++++************************aa')
		items = request.env['siat.invoice'].browse(_id)
		try:
			if len(items) <= 0:
				raise Exception('La factura no existe')
			invoice = items[0]
			service = ServiceInvoices()
			service.renovar(invoice)
			# service.send_customer_email_with_thread(invoice)
			return request.make_json_response({
				'status': 'ok',
				'code': 200,
				'data': None,
				'message': 'La factura fue reenviada correctamente'
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
	#***************************************************************

	@http.route(['/siat/invoices/<int:id>/reenviar'], type='http', auth='user', methods=['GET'])
	def forward(self, **params):
		self._check_session()
		_id = params.get('id')
		items = request.env['siat.invoice'].browse(_id)
		try:
			if len(items) <= 0:
				raise Exception('La factura no existe')
			invoice = items[0]
			service = ServiceInvoices()
			service.send_customer_email(invoice)
			# service.send_customer_email_with_thread(invoice)
			return request.make_json_response({
				'status': 'ok',
				'code': 200,
				'data': None,
				'message': 'La factura fue reenviada correctamente'
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



	
