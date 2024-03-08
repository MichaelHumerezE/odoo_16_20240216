from odoo import models, fields

class Branch(models.Model):
	_table = 'mb_siat_branches'
	_name = 'siat.branch'
	_description = 'Siat Branch model'

	company_id = fields.Many2one(
		comodel_name='res.company',
		string='Company',
		store=True,
		index=True,
	)
	codigo		= fields.Integer(string='Codigo SIN', required=True)
	nombre		= fields.Char(string='Nombre Sucursal', size=256, default=None)
	descripcion	= fields.Char(size=512, default=None)
	direccion	= fields.Char(size=256, required=False, default=None)
	ciudad		= fields.Char(size=256, required=True)
	puntosventa	= fields.One2many('siat.pos', 'sucursal_id')
