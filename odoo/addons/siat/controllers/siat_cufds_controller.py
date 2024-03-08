# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request, Controller
from odoo.osv.expression import AND
from odoo.tools import format_amount
# from odoo.addons.account.controllers.portal import PortalAccount

from ..libsiat import constants as siat_constants
from ..libsiat.classes.siat_exception import SiatException
from .siat_controller import SiatController

_logger = logging.getLogger(__name__)


class SiatCufdsController(Controller, SiatController):
	
	@http.route(['/siat/cufds', '/siat/cufds/sucursal/<int:sucursal>/puntoventa/<int:puntoventa>'], type='http', auth='user', methods=['GET'])
	def read_all(self, **params):
		self._check_session()
		sucursal = int(params.get('sucursal', 0))
		puntoventa = int(params.get('puntoventa', 0))
		
		items = request.env['siat.cufd'].readAll()
		
		return request.make_json_response({'status': 'ok', 'code': 200, 'data': items.read()})
