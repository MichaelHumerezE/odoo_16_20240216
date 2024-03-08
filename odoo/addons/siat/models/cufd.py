import datetime

from odoo import models, fields

class Cufd(models.Model):
	_table = 'mb_siat_cufd'
	_name = 'siat.cufd'
	_description = 'Siat CUFD records'

	company_id = fields.Many2one(
		comodel_name='res.company',
		string='Company',
		store=True,
		index=True,
	)
	codigo = fields.Char()
	codigo_control = fields.Char()
	direccion = fields.Char(size=512)
	sucursal_id = fields.Integer()
	puntoventa_id = fields.Integer()
	fecha_creacion = fields.Datetime()
	fecha_vigencia = fields.Datetime()

	def getLatest(self, company, sucursal=0, puntoventa=0):
		items = self.env['siat.cufd'].search([
			('company_id', '=', company),
			('sucursal_id', '=', sucursal),
			('puntoventa_id', '=', puntoventa)
		], order='fecha_vigencia DESC', limit=1)
		
		return items

	def readAll(self, limit=25):
		
		items = self.env['siat.cufd'].search([], order='id DESC', limit=limit)
		
		return items

	def isExpired(self):
		
		if datetime.datetime.now().timestamp() > self.fecha_vigencia.timestamp():
			return True
			
		return False

	def getByCode(self, code):
		
		items = self.env['siat.cufd'].search([('codigo', '=', code)], limit=1)
		
		if len(items) <= 0:
			return None
		
		return items[0]
