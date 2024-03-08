from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class SiatSaleOrder(models.Model):
    # _name = 'siat.sale.order'
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        print('SIAT HOOK INTO sale.order')
        moves = super(SiatSaleOrder, self)._create_invoices(grouped, final, date)

        return moves
