from odoo import models, fields
from .cufd import Cufd

from ..libsiat import constants as siat_constans
from .package import Package

class Event(models.Model):
	_table = 'mb_siat_eventos'
	_name = 'siat.event'
	_description = 'Event data model'
	
	# constants
	STATUS_OPEN 	= 'OPEN'
	STATUS_CLOSED 	= 'CLOSED'
	STATUS_VOID 	= 'VOID'

	company_id = fields.Many2one(
		comodel_name='res.company',
		string='Company',
		store=True,
		index=True,
	)
	evento_id = fields.Integer(required=True)
	sucursal_id = fields.Integer(required=True)
	puntoventa_id = fields.Integer(required=True)
	codigo_reception = fields.Char(size=256, default=None)
	descripcion = fields.Char(size=256, default=None)
	fecha_inicio = fields.Datetime(required=True)
	fecha_fin = fields.Datetime(required=False, default=None)
	cufd = fields.Char(size=256, required=False, default=None)
	cufd_evento = fields.Char(size=256, required=True)
	codigo_recepcion_paquete = fields.Char(size=512, required=False, default=None)
	estado_recepcion = fields.Char(size=64, required=False, default=None)
	status = fields.Char(size=64, required=True)
	data = fields.Text(required=False)
	last_invoices_count = fields.Integer(default=0)
	invoices = fields.One2many('siat.invoice', 'evento_id')
	packages = fields.One2many('siat.package', 'event_id')

	def get_cufd(self) -> Cufd:
		items = self.env['siat.cufd'].search([('codigo', '=', self.cufd)], limit=1)
		if len(items) <= 0:
			return None

		return items[0]

	def get_cufd_evento(self) -> Cufd:
		items = self.env['siat.cufd'].search([('codigo', '=', self.cufd_evento)], limit=1)
		if len(items) <= 0:
			return None

		return items[0]

	def get_invoices(self):
		# items = self.env['siat.invoice'].search([('evento_id')])

		items = self.invoices
		count = len(self.invoices)
		self.write({'last_invoices_count': count})

		return items

	def get_pending_invoices(self):
		items = self.env['siat.invoice'].search([
			('evento_id', '=', self.id),
			'|',
			('siat_id', '=', None),
			('siat_id', '=', '')
		])

		return items

	def get_packages(self, rebuild=False):
		if len(self.packages) > 0 and rebuild is False:
			# self.set_packages_invoices(self.packages)
			return self.packages

		# self.env['siat.'].flush_model(['partner_id'])
		self.env.cr.execute('DELETE FROM mb_siat_event_packages WHERE event_id = %s', [self.id])

		query = '''
		SELECT COUNT(id) as total_facturas, codigo_documento_sector, tipo_factura_documento 
		FROM mb_invoices
		WHERE evento_id::INT = %s
		AND tipo_emision::INT = %s
		GROUP BY codigo_documento_sector, tipo_factura_documento
		'''
		self.env.cr.execute(query, [self.id, siat_constans.TIPO_EMISION_OFFLINE])
		items = self.env.cr.fetchall()
		packages = []
		for item in items:
			if int(item[0]) <= 0:
				continue
			pkg = self.env['siat.package'].create({
				'event_id': self.id,
				'invoice_type': item[2],
				'sector_document': item[1],
				'status': Package.STATUS_OPEN
			})
			packages.append( pkg [0])
			# mark invoices

		Event.set_packages_invoices(packages)
		'''
		invoices = self.env['siat.invoice'].search([
			('evento_id', '=', self.id),
			('codigo_documento_sector', '=', item.get('codigo_documento_sector'))
		])
		'''
		return packages

	@staticmethod
	def set_packages_invoices(packages: list):
		for pkg in packages:
			pkg.mark_invoices()

	def create_invoice_packets(self):
		pass
