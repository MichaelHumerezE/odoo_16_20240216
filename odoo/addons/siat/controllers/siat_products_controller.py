# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request, Controller
from odoo.osv.expression import AND
from odoo.tools import format_amount
# from odoo.addons.account.controllers.portal import PortalAccount

from ..libsiat import constants as siat_constants
from ..libsiat.classes.siat_exception import SiatException
from ..services.service_siat_sync import ServiceSiatSync
from ..resources.resource_product import ResourceProduct
from .siat_controller import SiatController

_logger = logging.getLogger(__name__)


class SiatProductsController(Controller, SiatController):
	
	@http.route(['/siat/products/search', '/siat/products/search/<string:keyword>'], type='http', auth='public', methods=['GET', 'POST'])
	def search_product(self, **params):
		self._check_session()
		keyword = params.get('keyword', '')
		if not keyword:
			return request.make_json_response({'status': 'ok', 'code': 200, 'data': [], 'keyword': keyword})
		'''
		query = “””SELECT * FROM res_partner”””
		self.env.cr.execute(query)
		self.env.cr.fetchall()
		'''
		
		search_domain = [
			'|', '|', '|', 
			('default_code', 'ilike', keyword), 
			('product_variant_ids.default_code', 'ilike', keyword),
			('name', 'ilike', keyword), 
			('barcode', 'ilike', keyword)
		]
		products = request.env['product.template'].search(
			#[
			#	('default_code', 'ilike', keyword),
				# '|',
				# ('product_tmpl_id.name', 'ilike', keyword),
				# ('product_tmpl_id.default_code', 'ilike', keyword),
				# '&',
				# ('product_tmpl_id.unidad_medida', '>', '0'),
				# ('product_tmpl_id.codigo_producto_sin', '>', '0'),
			#],
			search_domain, 
			order='id ASC', 
			limit=20
		)
		length = len( products )
		items = []
		for product in products:
			resource = ResourceProduct(product)
			items.append( resource.dict() )
			
		# if length > 0:
		#	items.append( product[0].read ) 
		
		return request.make_json_response({
			'status': 'ok', 
			'code': 200, 
			'length': length,
			'data': items
		})
