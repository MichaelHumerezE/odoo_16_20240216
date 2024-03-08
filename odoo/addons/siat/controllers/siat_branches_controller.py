# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request, Controller
from odoo.tools import format_amount

from .siat_controller import SiatController

_logger = logging.getLogger(__name__)


class SiatBranchesController(Controller):

	@http.route(['/siat/branches', '/siat/sucursales'], type='http', auth='user', methods=['GET'])
	def read_all(self, **params):
		# self._check_session()
		items = request.env['siat.branch'].search([])

		return request.make_json_response({'status': 'ok', 'code': 200, 'data': items.read()})
