# -*- coding: utf-8 -*-
import logging
import json

from odoo import http, _
from odoo.http import request, Controller
from odoo.osv.expression import AND
from odoo.tools import format_amount
# from odoo.addons.account.controllers.portal import PortalAccount

from ..libsiat import constants as siat_constants
from ..libsiat.classes.siat_exception import SiatException
from ..services.service_siat_sync import ServiceSiatSync
from ..resources.resource_customer import ResourceCustomer
from .siat_controller import SiatController
_logger = logging.getLogger(__name__)

class SiatCustomerController(Controller, SiatController):
	
	@http.route(['/siat/customers/search'], type='http', auth='user', methods=['POST'], csrf=False)
	def search(self, **params):
		self._check_session()
		#keyword = params.get('keyword', '')
		# print(params)
		data = json.loads(request.httprequest.data)
		# data = request.jsonrequest
		keyword = data.get('keyword', '')
		
		if not keyword:
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': []})
			
		items = request.env['res.partner'].search(
			[
				('name', 'ilike', keyword), 
				('type', '=', 'contact')
			], 
			order='name ASC', 
			limit=20
		)
		resources = []
		
		for item in items:
			res = ResourceCustomer(item.read()[0])
			resources.append( res.dict() )
			
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': resources})
