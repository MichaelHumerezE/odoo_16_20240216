# -*- coding: utf-8 -*-
from odoo import fields, models


class ActWindowView(models.Model):
	_inherit = 'ir.actions.act_window.view'

	view_mode = fields.Selection(
		selection_add=[('siat_view', "Hello World From Action")], 
		ondelete={'siat_view': 'set default'}, 
		default='siat_view'
	)
