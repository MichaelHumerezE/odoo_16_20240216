from odoo import models, fields

class PointOfSale(models.Model):
	_table = 'mb_siat_puntos_venta'
	_name = 'siat.pos'
	_description = 'Siat Point of Sale model'
	_rec_name = 'nombre'

	company_id = fields.Many2one(
		comodel_name='res.company',
		string='Company',
		store=True,
		index=True,
	)
	sucursal_id 		= fields.Many2one('siat.branch')
	codigo 				= fields.Integer(required=True)
	codigo_sucursal 	= fields.Integer(required=True)
	tipo_id 			= fields.Integer(required=True)
	tipo_descripcion 	= fields.Char(size=256, required=True)
	nombre 				= fields.Char(size=256, default=None)
	descripcion 		= fields.Char(size=512, default=None)
	direccion 			= fields.Char(size=256, required=False, default=None)
	ciudad 				= fields.Char(size=256, required=True)
	telefono 			= fields.Char(size=64, required=True)

	def get_by_code(self, code):
		items = self.env['siat.pos'].search([('codigo', '=', code)], limit=1)

		if len(items) <= 0:
			return None

		return items[0]

