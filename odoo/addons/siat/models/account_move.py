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

        print('TO POST POST', to_post.read())
        
        #MODIFY - Multi Branch and  Multi Point of Sale
        pos = to_post.ref.split('/')
        pos = self.env['pos.config'].search(
            domain=[('name', '=', pos[0])],
            limit=1,
        )
        #************************************************
        #MODIFY - Verify Relation POS with siat_pos
        if not pos.siat_pos_id:
            raise Exception('Punto de Venta no asociado a ningún Punto de Venta de SIAT, Vaya a ajustes para configurar la asociacíon correctamente')
        #***********************************************

        invoiceData = {
            'codigo_documento_sector': 1,
            'codigo_sucursal': pos.siat_pos_id.sucursal_id.codigo,
            'punto_venta': pos.siat_pos_id.codigo,
            'customer_id': to_post.partner_id.id,
            'customer': to_post.partner_id.name,
            'tipo_documento_identidad': 1,
            'nit_ruc_nif': to_post.partner_id.vat,
            'complemento': '',
            'codigo_metodo_pago': 1,
            'numero_tarjeta': None,
            'total': round(to_post.amount_total,2),
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
