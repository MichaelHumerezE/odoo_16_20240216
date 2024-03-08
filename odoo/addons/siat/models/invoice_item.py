from odoo import models, fields

from ..services.service_siat_sync import ServiceSiatSync


class InvoiceItem(models.Model):
	_table = 'mb_invoice_items'
	_name = 'siat.invoiceitem'
	_description = 'Invoice Item data model'

	invoice_id = fields.Many2one('siat.invoice')
	product_id = fields.Many2one('product.product')
	product_code = fields.Char(size=64, required=True)
	product_name = fields.Char(size=512, required=True)
	price = fields.Float(default=0)
	quantity = fields.Float(default=1)
	subtotal = fields.Float(required=True)
	discount = fields.Float(required=True)
	total = fields.Float(required=True)
	codigo_actividad = fields.Char(size=64, required=True)
	codigo_producto_sin = fields.Integer(required=True)
	unidad_medida = fields.Integer(required=True)
	numero_seria = fields.Char(size=64, required=False, default=None)
	numero_imei = fields.Char(size=64, required=False, default=None)
	nandina = fields.Char(size=64, required=False, default=None)

	@staticmethod
	def get_unidad_medida(codigo_unidad_medida: int):
		# invoice_item = self[0]
		service = ServiceSiatSync()
		return service.buscar_unidad_medida(codigo_unidad_medida)
