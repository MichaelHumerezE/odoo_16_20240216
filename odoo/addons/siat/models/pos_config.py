from odoo import fields, models, api, _


class SiatPosConfig(models.Model):
    _inherit = 'pos.config'

    siat_pos_id = fields.Many2one(
        'siat.pos',
        store=True,
        index=True,
        # domain="[('company_id', '=', company_id)]",
    )
