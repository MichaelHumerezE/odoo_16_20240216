from odoo import fields, models, api, _
import qrcode
import base64
import io
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

from ..services.service_invoices import ServiceInvoices


class SiatPosOrder(models.Model):

    _inherit = 'pos.order'

    def _generate_pos_order_invoice(self):
        company_id = int(request.httprequest.cookies.get('cids'))
        request.update_context(allowed_company_ids=[company_id])
        '''
        invoiceRequestData = None

        for order in self:
            # print(order.read())

            invoiceRequestData = {
                'codigo_documento_sector': 1,
                'codigo_sucursal': 0,
                'punto_venta': 0,
                'customer_id': order.partner_id.id,
                'customer': order.partner_id.name,
                'tipo_documento_identidad': 1,
                'nit_ruc_nif': order.partner_id.vat,
                'complemento': '',
                'codigo_metodo_pago': 1,
                'numero_tarjeta': None,
                'total': order.amount_total,
                'codigo_moneda': 1,
                'tipo_cambio': 1,
                'monto_giftcard': 0,
                'discount': 0,
                'data': {'excepcion': 0},
                'items': []
            }
            for line in order.lines:
                # print(line.read())
                # print(line.product_id.read())

                product_code = line.product_id.default_code
                if not product_code:
                    line.product_id.code

                item = {
                    'product_id': line.product_id.id,
                    'product_code':  product_code,
                    'product_name': line.product_id.name, # line.product_id.display_name,
                    'quantity': line.qty,
                    'unidad_medida': line.product_id.unidad_medida,
                    'codigo_actividad': line.product_id.actividad_economica,
                    'codigo_producto_sin': line.product_id.codigo_producto_sin,
                    'price': line.price_unit,
                    'discount': line.discount,
                    'numero_serie': '',
                    'numero_imei': '',
                }
                invoiceRequestData['items'].append(item)

        print('INVOICE DATA: ', invoiceRequestData)
        print('CURRENT USER ID: ', request.env.uid)
        print('CURRENT COMPANY ID: ', request.env.company.id)
        # service = ServiceInvoices()
        # invoice = service.create(invoiceRequestData)
        # print(invoice.read())
        # print('')

        # raise ValidationError(_('Debe registrar NIT/CI o Razón Social para facturar'))
        '''
        data = super(SiatPosOrder, self)._generate_pos_order_invoice()
        print('POS ORDER DATA', data)
        #for order in self:
        #    order.account_move.write({'siat_invoice_id': invoice.id})

        return data