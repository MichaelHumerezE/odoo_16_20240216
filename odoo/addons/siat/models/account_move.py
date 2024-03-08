from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

from ..services.service_invoices import ServiceInvoices

class SiatAccountMove(models.Model):
    _inherit = 'account.move'

    siat_invoice_id = fields.Many2one('siat.invoice')

    def post(self):
        res = super().post()
        raise ValidationError(_('Debe registrar NIT/CI o Razón Social para facturar'))

        return res

    def _post(self, soft=True):
        to_post = super()._post(soft)

        if to_post.move_type != 'out_invoice':
            return to_post

        print('TO POST', to_post.read())

        invoiceData = {
            'codigo_documento_sector': 1,
            'codigo_sucursal': 0,
            'punto_venta': 0,
            'customer_id': to_post.partner_id.id,
            'customer': to_post.partner_id.name,
            'tipo_documento_identidad': 1,
            'nit_ruc_nif': to_post.partner_id.vat,
            'complemento': '',
            'codigo_metodo_pago': 1,
            'numero_tarjeta': None,
            'total': to_post.amount_total,
            'codigo_moneda': 1,
            'tipo_cambio': 1,
            'monto_giftcard': 0,
            'discount': 0,
            'data': {'excepcion': 0},
            'items': []
        }
        for line in to_post.invoice_line_ids:
            product_code = line.product_id.default_code
            if not product_code:
                line.product_id.code

            item = {
                'product_id': line.product_id.id,
                'product_code': product_code,
                'product_name': line.product_id.name,  # line.product_id.display_name,
                'quantity': line.quantity,
                'unidad_medida': line.product_id.unidad_medida,
                'codigo_actividad': line.product_id.actividad_economica,
                'codigo_producto_sin': line.product_id.codigo_producto_sin,
                'price': line.price_unit,
                'discount': line.discount,
                'numero_serie': '',
                'numero_imei': '',
            }
            invoiceData['items'].append(item)

        print('INVOICE DATA', invoiceData)

        service = ServiceInvoices()
        invoice = service.create(invoiceData)
        print('ACCOUNT MOVE INVOICE', invoice)
        if invoice is not None:
            to_post.write({
                'siat_invoice_id': invoice.id
            })

        return to_post
