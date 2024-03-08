from odoo import models, fields, api


class SiatConfig(models.Model):
    _table = 'siat_config'
    _name = 'siat.config'
    _description = 'Siat Config'

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        store=True,
        index=True,
    )
    nombre_sistema = fields.Char(size=128)
    codigo_sistema = fields.Char(size=128)
    nit = fields.Char(size=128)
    razon_social = fields.Char(size=256)
    modalidad = fields.Integer(default=1)
    ambiente = fields.Integer(default=2)
    token_delegado = fields.Text()
    tipo_impresion = fields.Char(size=32)
    cafc = fields.Text()
    priv_cert = fields.Char(size=512)
    pub_cert = fields.Char(size=512)

