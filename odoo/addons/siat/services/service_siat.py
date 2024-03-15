# -*- coding: utf-8 -*-
import os
import traceback
# from ..libsiat import constants as siat_constants
from odoo.http import request
from .. import constants

class ServiceSiat:

	@staticmethod
	def check_session():
		company_id = int(request.httprequest.cookies.get('cids'))
		request.update_context(allowed_company_ids=[company_id])

	def getConfig(self, codigo_sucursal):
		'''
		cfg = {
			'modalidad': siat_constants.MOD_COMPUTARIZADA_ENLINEA,
			# 'modalidad': constants.MOD_ELECTRONICA_ENLINEA,
			'ambiente': siat_constants.AMBIENTE_PRUEBAS,
			'codigoSistema': '722A170272B644A27ED6F67',
			'nombreSistema': 'Factura 1Byte',
			'nit': 13492810016,
			'razonSocial': 'HUAYCHO CUIZA MANUEL ALFREDO',
			'tipo': 'PROVEEDOR',
			'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJNYW51ZWxBSEMiLCJjb2RpZ29TaXN0ZW1hIjoiNzIyQTE3MDI3MkI2NDRBMjdFRDZGNjciLCJuaXQiOiJINHNJQUFBQUFBQUFBRE0wTnJFMHNqQTBNREEwQXdBVTZzdC1Dd0FBQUE9PSIsImlkIjozMDE0ODIxLCJleHAiOjE2OTYxMTg0MDAsImlhdCI6MTY2NTA4ODU3NCwibml0RGVsZWdhZG8iOjEzNDkyODEwMDE2LCJzdWJzaXN0ZW1hIjoiU0ZFIn0.7WvPt7JmTmK94G1LONeaTuszfj4jsbfG2J3DOVtsPDigKVpmDD75LD1PPr-4uIiniQW7st_E_FDjez1EnXzNwQ',
			'pubCert': '{0}{1}certs{1}{2}'.format(siat_constants.BASE_DIR, siat_constants.SB_DS, 'NUBETIC_SRL_CER.pem'),
			'privCert': '{0}{1}certs{1}{2}'.format(siat_constants.BASE_DIR, siat_constants.SB_DS, 'RUBEN_BALTAZAR_BALDERRAMA.pem'),
			'ciudad': 'Santa Cruz',
			'telefono': '77739265'
		}
		'''
		cfg = {}
		try:
			rows = request.env['siat.config'].search([('company_id', '=', request.env.company.id)], limit=1)
			if len(rows) <= 0:
				raise Exception('La compañia ('+ str(request.env.company.id) +') no tiene configuracion SIAT')
			cfg = rows.read()[0]
			cfg['token'] = cfg['token_delegado']
			cfg['codigoSistema'] = cfg['codigo_sistema']
			cfg['codigoAmbiente'] = cfg['ambiente']
			cfg['nombreSistema'] = cfg['nombre_sistema']
			cfg['razonSocial'] = cfg['razon_social']
			#MODIFY - Load Branch
			branch = request.env['siat.branch'].search([('codigo', '=', codigo_sucursal)], limit=1)
			if not branch:
				raise Exception('Sucursal no encontrada verificque los datos de la sucursal perteneciente al punto de venta')
			#**********************************
			cfg['ciudad'] = branch.ciudad
			cfg['telefono'] = branch.descripcion
			cfg['pubCert'] = '{0}/cid-{1}/certificado.pem'.format(constants.DATA_DIR, request.env.company.id)
			cfg['privCert'] = '{0}/cid-{1}/llave_privada.pem'.format(constants.DATA_DIR, request.env.company.id)
			# print('SIAT CONFIG', cfg)
		except Exception as e:
			print('SIAT CONFIG ERROR', str(e))
			print('USER COMPANY', request.env.user.company_id.id)
			# print(request._context.get('allowed_company_ids'))
			# print(traceback.print_exc())

		return cfg

	def file_get_contents(self, filename):
	
		if os.path.isfile(filename) == False:
			return ''
		
		with open(filename, 'r') as f:
			return f.read()
		
