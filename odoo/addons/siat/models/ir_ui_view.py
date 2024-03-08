# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
	_inherit = 'ir.ui.view'

	type = fields.Selection(
		selection_add=[('siat_view', 'Siat View')],
		ondelete={'siat_view': 'set default'},
		default='siat_view'
	)
