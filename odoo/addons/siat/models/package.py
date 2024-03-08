from odoo import models, fields

import json
from ..libsiat import constants as siat_constans

class Package(models.Model):
    _table          = 'mb_siat_event_packages'
    _name           = 'siat.package'
    _description    = 'Event package data model'

    # status
    STATUS_OPEN     = 'OPEN'
    STATUS_CLOSED   = 'CLOSED'
    STATUS_PENDING  = 'PENDING'

    event_id = fields.Many2one('siat.event')
    invoice_type = fields.Integer(required=True)
    sector_document = fields.Integer(required=True)
    reception_code = fields.Char(size=128)
    reception_status = fields.Char(size=64)
    reception_date = fields.Datetime()
    status = fields.Char(size=32)
    data = fields.Text(required=False)
    invoices = fields.One2many('siat.invoice', 'package_id')

    def mark_invoices(self):
        for _pkg in self:
            pkg = _pkg
            dml = '''
            UPDATE mb_invoices SET package_id = {0}
            WHERE evento_id = {1}
            AND codigo_documento_sector = {2}
            AND tipo_factura_documento = {3}
            '''.format(pkg.id, pkg.event_id[0].id, pkg.sector_document, pkg.invoice_type)
            print('DML', dml)
            self.env.cr.execute(dml, [])

    def get_pending_invoices(self):
        items = self.env['siat.invoice'].search([
            ('package_id', '=', self.id),
            '|',
            ('siat_id', '=', None),
            ('siat_id', '=', ''),
        ])

        return items

    def get_data(self):
        data_str = self.data
        if not data_str:
            return {}

        return json.loads(data_str)

    
