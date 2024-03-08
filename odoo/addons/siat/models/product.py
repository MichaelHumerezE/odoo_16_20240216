# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.http import request
from odoo.exceptions import UserError
from itertools import groupby
from operator import itemgetter
from datetime import date
from ..services.service_siat_sync import ServiceSiatSync


def _get_actividades(arg):

	data = [('', '-- actividade economica --')]
	try:
		service = ServiceSiatSync()
		res = service.sync_actividades()
		if res is None:
			return data
		for actividad in res['RespuestaListaActividades']['listaActividades']:
			data.append( (actividad.get('codigoCaeb'), actividad.get('descripcion')) )
	except Exception as e:
		print('ERROR __get_actividades', str(e))

	return data


def _get_unidades_medida(arg):
	# print('REQUEST', type(request), hasattr(request, 'env'))
	data = [('0', '-- unidad medida --')]

	try:
		service = ServiceSiatSync()
		res = service.sync_unidades_medida()
		if res is None:
			return data
		for actividad in res['RespuestaListaParametricas']['listaCodigos']:
			data.append( (str(actividad.get('codigoClasificador')), actividad.get('descripcion')) )
	except Exception as e:
		print('ERROR __get_unidades_medida', str(e))

	return data


def _get_productos_sin(arg):
	# print('ARG', arg)
	codigos_sin = [('0', '-- producto sin --')]
	try:
		service = ServiceSiatSync()
		res = service.sync_productos_servicios()
		if res is None:
			return codigos_sin
		for item in res['RespuestaListaProductos']['listaCodigos']:
			codigos_sin.append(
				('{0}'.format( item.get('codigoProducto') ), '{0} ({1})'.format(item.get('descripcionProducto'), item.get('codigoActividad')) )
			)
	except Exception as e:
		print('ERROR __get_productos_sin', str(e))

	return codigos_sin


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	unidad_medida = fields.Integer(default='0')
	unidad_medida_selector = fields.Selection(_get_unidades_medida, store=False, readonly=False, compute='_compute_unidad_medida_selector')
	#	default='', store=False,  ,
	#	precompute=True,
	#	prefetch=False
	#)
	actividad_economica = fields.Selection(_get_actividades, readonly=False)
	codigo_producto_sin = fields.Integer(default=0)
	codigo_producto_sin_selector = fields.Selection(
		_get_productos_sin,
		store=False,
		readonly=False,
		compute='_compute_codigo_producto_sin_selector'
	)
	siat_invoice_item_id = fields.One2many('siat.invoiceitem', 'product_id')

	@api.depends('unidad_medida')
	def _compute_unidad_medida_selector(self):
		try:
			self.unidad_medida_selector = str(self.unidad_medida)
		except:
			pass
		
		#for record in self:
		#	record.unidad_medida_selector = record.unidad_medida # type_mapping.get(record.unidad_medida, record.unidad_medida)

	@api.depends('codigo_producto_sin')
	def _compute_codigo_producto_sin_selector(self):
		try:
			self.codigo_producto_sin_selector = str( self.codigo_producto_sin )
		except:
			pass
	
	def _search_productos_sin(self, operator, value):
		print('SEARCH PRODUCTOS SIN')
		print(operator)
		print(value)
		
		return [('name', operator, value)]
		
	@api.onchange('unidad_medida_selector')
	def _onchange_unidad_medida_selector(self):
		self.unidad_medida = int(self.unidad_medida_selector)
		
	'''
	@api.onchange('actividad_economica')
	def _onchange_actividad_economica(self):
		print('CHANGED ACTIVIDAD ECONOMICA: {0}'.format(self.actividad_economica))
		if self.actividad_economica == False:
			return
		
		print(type(self.actividad_economica))
		for record in self:
			print(type(record))
			print(type(record.codigo_producto_sin_selector))
			record.update(res)
			# record.codigo_producto_sin_selector = _get_productos_sin(self.actividad_economica)
	'''
	
	@api.onchange('codigo_producto_sin_selector')
	def _onchange_codigo_producto_sin_selector(self):
		if self.codigo_producto_sin_selector == False:
			return
			
		codigo = self.codigo_producto_sin_selector
		
		'''
		selected_code = self.codigo_producto_sin_selector.replace('"', '').replace("'", '')
		codigo = selected_code
		
		if ':' in selected_code:
			data = selected_code.split(':')
			codigo = data[1]
		'''
		self.codigo_producto_sin = int( codigo )
		
			
