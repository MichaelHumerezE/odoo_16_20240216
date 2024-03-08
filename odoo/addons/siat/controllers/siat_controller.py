# -*- coding: utf-8 -*-
import logging
#from abc import ABC, abstractmethod

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount

_logger = logging.getLogger(__name__)


class SiatController():

	def _check_session(self):
		company_id = int(request.httprequest.cookies.get('cids'))
		print('COMPANY ID: ', company_id)
		request.update_context(allowed_company_ids=[company_id])
		# for key, value in request.session.items():
		#	print("----------->", key, value)
		#print(request.env.company)
