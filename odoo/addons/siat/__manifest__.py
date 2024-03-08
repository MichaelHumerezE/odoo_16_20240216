# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
	'name': 'FacturacionSIAT',
	'version': '1.0.6',
	'summary': 'Facturacion SIAT',
	'sequence': 3,
	'author': 'SinticBolivia',
	'description': """
	""",
	'category': 'Accounting/Accounting',
	'website': 'https://sinticbolivia.net',
	# 'images': [],
	'depends': ['base', 'stock_account', 'mail', 'point_of_sale', 'pos_sale'],
	'data': [
		'security/ir.model.access.csv',
		'views/siat_view_assets.xml',
		'views/sync_view.xml',
		'views/pos_config.xml',
		# 'views/config_view.xml',
		'views/branch_view.xml',
		'views/events_view.xml',
		'views/product_view.xml',
		'views/report_invoice.xml',
		'views/invoice_email_template.xml',
		'views/account_report_invoice.xml',
		'views/menu_views.xml',
	],
	'assets': {
		'web.assets_backend': [
			'siat/static/src/js/siat_view.js',
		],
	},
	'installable': True,
	'application': True,
	'auto_install': True,
	'license': 'LGPL-3',
}
