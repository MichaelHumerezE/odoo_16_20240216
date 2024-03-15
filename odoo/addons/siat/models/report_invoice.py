from odoo import api, models
from odoo.http import request

from ..services.service_invoices import ServiceInvoices
from ..libsiat.invoices.siatinvoice import SiatInvoice
from ..libsiat import functions as siat_functions
from ..models.invoice_item import InvoiceItem
from datetime import datetime, timedelta

class ReportInvoice(models.AbstractModel):
	_name = 'report.siat.siat_invoice_template'
	_description = 'Siat Report Invoice'

	def _get_report_values(self, docids, data=None):
		company_id = int(request.httprequest.cookies.get('cids'))
		request.update_context(allowed_company_ids=[company_id])

		invoices = self.env['siat.invoice'].browse( docids )
		invoice = invoices[0]
		cufds = self.env['siat.cufd'].search([('codigo', '=', invoice.cufd)], limit=1)
		
		#for invoice in invoices:
		#	invoice.amount_text = 'literal del monto'
		service = ServiceInvoices()
		#MODIFY - Load Branch
		sucursalBD = self.env['siat.branch'].search([('codigo', '=', invoice.codigo_sucursal)], limit=1)
		if(invoice.codigo_sucursal == 0):
			sucursal = sucursalBD.nombre
		else:
			sucursal = 'Sucursal No. ' + str(invoice.codigo_sucursal)
		ciudad = sucursalBD.ciudad
		telefono = sucursalBD.descripcion
		#************************************************
		siat_url = SiatInvoice.buildUrl(invoice.nit_emisor, invoice.cuf, invoice.invoice_number, invoice.ambiente)
		qr64 = siat_functions.sb_build_qr(siat_url)
		# print('SIAT URL: ', siat_url, 'QR64: ', qr64.decode('utf8'))
		amount_text = siat_functions.sb_numeroToLetras(invoice.total) + ' BOLIVIANOS'
		return {
			'docs': invoices,
			'amount_text': amount_text, # .encode('ascii', 'xmlcharrefreplace'),
			'cufd': cufds[0] if len(cufds) > 0 else None,
			'siat_config': service.getConfig(invoice.codigo_sucursal),
			'sucursal': sucursal,
			'ciudad': ciudad,
			'telefono': telefono,
			'qr_buffer': 'data:image/png;base64,{0}'.format(qr64.decode('utf8')),
			'get_unidad_medida': InvoiceItem.get_unidad_medida
		}


class ReportInvoiceTicket(ReportInvoice):
	_name = 'report.siat.siat_invoice_template_ticket'
	_description = 'Siat Report Invoice'
