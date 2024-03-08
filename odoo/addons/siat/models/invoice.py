from odoo import models, fields, api
import json

from ..libsiat.invoices.siatinvoice import SiatInvoice

class Invoice(models.Model):
	_table = 'mb_invoices'
	_name = 'siat.invoice'
	_description = 'Invoice data model'

	customer_id = fields.Integer()
	# customer_id = fields.Many2one('res.partner', 'id')
	customer_name = fields.Char()
	nit_ruc_nif = fields.Char()
	subtotal = fields.Float(digits=(12, 2))
	total_tax = fields.Float(digits=(12, 2))
	discount = fields.Float(digits=(12, 2))
	monto_giftcard = fields.Float(digits=(12, 2))
	total = fields.Float()
	invoice_number = fields.Integer()
	control_code = fields.Char()
	invoice_datetime = fields.Datetime()
	void_datetime = fields.Datetime()
	status = fields.Char()
	codigo_sucursal = fields.Integer()
	punto_venta = fields.Integer()
	actividad_economica = fields.Integer()
	codigo_documento_sector = fields.Integer()
	tipo_documento_identidad = fields.Integer()
	codigo_metodo_pago = fields.Integer()
	codigo_moneda = fields.Integer()
	cufd = fields.Char()
	cuf = fields.Char()
	cafc = fields.Char()
	complemento = fields.Char()
	numero_tarjeta = fields.Char()
	tipo_cambio = fields.Float(digits=(12, 2))
	evento_id = fields.Integer()
	package_id = fields.Integer()
	siat_id = fields.Char()
	tipo_emision = fields.Char()
	tipo_factura_documento = fields.Integer()
	nit_emisor = fields.Char()
	ambiente = fields.Integer()
	leyenda = fields.Char()
	data = fields.Text()
	items = fields.One2many('siat.invoiceitem', 'invoice_id')
	account_move_id = fields.One2many('account.move', 'siat_invoice_id')
	company_id = fields.Many2one(
		comodel_name='res.company',
		string='Company',
		# compute='_compute_company_id', inverse='_inverse_company_id',
		store=True,
		# readonly=False,
		# precompute=True,
		index=True,
	)

	STATUS_ISSUED = 'ISSUED'
	STATUS_VOID = 'VOID'

	def nextInvoiceNumber(self, company_id):
		count = self.env['siat.invoice'].search_count([('company_id', '=', company_id)])
		
		return count + 1

	def get_data(self, key=None):
		data = None

		if not self.data:
			data = {}
		else:
			data = json.loads(self.data)

		if type(data) is not dict: # or type(data) is list:
			data = {}

		if key:
			return data.get(key, None)

		return data

	def set_data(self, key, value):
		data = self.get_data()
		data[key] = value

		self.data = data

		return True

	def _prepare_data(self, data):
		if (type(data) is dict or type(data) is list):
			return json.dumps(data)
		return data

	@api.model # _create_multi
	def create(self, vals_list):
		if 'data' in vals_list:
			vals_list['data'] = self._prepare_data(vals_list['data'])

		return super(Invoice, self).create(vals_list)

	@api.model
	def write(self, values):
		if 'data' in values:
			values['data'] = self._prepare_data(values['data'])

		return super(Invoice, self).write(values)

	def get_customer(self):
		items = self.env['res.partner'].browse([self.customer_id])

		if len(items) <= 0:
			return None

		return items[0]

	def get_total(self):

		return '{0:,.2f}'.format(self.total)

	def get_siat_url(self):
		return SiatInvoice.buildUrl(self.nit_emisor, self.cuf, self.invoice_number, self.ambiente)

	def get_invoice_number(self):

		return self.invoice_number

	def get_cuf_chunked(self, separator=''):
		length = 30
		chunks = [self.cuf[i:i+length] + separator for i in range(0, len(self.cuf), length)]

		return "\n".join(chunks)
