# -*- coding: utf-8 -*-
from odoo import models, fields, api

from ..libsiat import functions as siat_functions
from ..libsiat.invoices.siatinvoice import SiatInvoice
from ..models.invoice_item import InvoiceItem
from ..services.service_invoices import ServiceInvoices

class ReportInvoiceWithPayment(models.AbstractModel):

    _name = 'report.account.report_invoice_with_payments'
    _inherit = 'report.account.report_invoice'
    # _name = 'report.siat.report_invoice_with_payments'
    # _inherit = 'report.account.report_invoice_with_payments'
    _description = 'Adicionar campos necesarios para la factura modulo account'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = super()._get_report_values(docids, data)
        service = ServiceInvoices()
        cufds = self.env['siat.cufd'].search([('codigo', '=', data['docs'].siat_invoice_id.cufd)], limit=1)
        print(cufds)
        siat_url = SiatInvoice.buildUrl(
            data['docs'].siat_invoice_id.nit_emisor,
            data['docs'].siat_invoice_id.cuf,
            data['docs'].siat_invoice_id.invoice_number,
            data['docs'].siat_invoice_id.ambiente
        )
        qr64 = siat_functions.sb_build_qr(siat_url)
        data['qr_buffer'] = 'data:image/png;base64,{0}'.format(qr64.decode('utf8'))
        data['amount_text'] = siat_functions.sb_numeroToLetras(data['docs'].siat_invoice_id.total) + ' BOLIVIANOS'
        data['get_unidad_medida'] = InvoiceItem.get_unidad_medida
        data['siat_config'] = service.getConfig()
        data['cufd'] = cufds # [0] if len(cufds) > 0 else None,
        # print('REPORT INVOICE DATA', data)
        return data