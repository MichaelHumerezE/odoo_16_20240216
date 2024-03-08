# -*- coding: utf-8 -*-
import logging
import json
import traceback

from odoo import http, _
from odoo.http import request, Controller

from ..services.service_siat_operations import ServiceSiatOperations
from .siat_controller import SiatController
from ..models.branch import Branch

_logger = logging.getLogger(__name__)


class SiatPuntosVentaController(Controller, SiatController):

    @http.route(['/siat/puntos-venta'], type='http', auth='user', methods=['GET'])
    def read_all(self, sucursal=0, page=1, limit=25):
        self._check_session()
        from .siat_controller import SiatController
        items = request.env['siat.pos'].search([], order='id desc', limit=limit)

        '''
        for event in events:
            resource = ResourceEvent(event)
            items.append(resource.dict())
        '''
        return request.make_json_response({
            'status': 'ok',
            'code': 200,
            'data': items.read()
        })

    @http.route(['/siat/puntos-venta'], type='http', auth='user', methods=['POST'], csrf=False)
    def create(self, **params):
        self._check_session()
        data = json.loads(request.httprequest.data)
        codigo_sucursal = data.get('sucursal_id', 0)
        tipo = data.get('tipo_id')
        descripcion = data.get('tipo')
        nombre = data.get('nombre')

        try:
            sucursal_id = 0

            if codigo_sucursal > 0:
                sucursal = request.env['siat.branch'].search([('codigo', '=', codigo_sucursal)], limit=1)
                if len(sucursal) <= 0:
                    raise Exception('La sucursal no existe')
                sucursal_id = sucursal[0].id

            service = ServiceSiatOperations()
            pos = service.registrar_puntoventa(sucursal_id, codigo_sucursal, tipo, nombre, descripcion)

            return request.make_json_response({
                'status': 'ok',
                'code': 200,
                'data': pos.read()[0]
            })
        except Exception as e:
            print(traceback.print_exc())
            code = 500
            return request.make_json_response({
                'status': 'error',
                'code': code,
                'data': None,
                'error': str(e)
            }, status=code)


    @http.route(['/siat/puntos-venta/sync'], type='http', auth='user', methods=['GET'])
    def sync(self, sucursal=0, **params):
        self._check_session()
        try:
            service = ServiceSiatOperations()
            res = service.consulta_puntos_venta(sucursal)
            print(res)
            for item in res['listaPuntosVentas']:
                pos = request.env['siat.pos'].get_by_code(item['codigoPuntoVenta'])
                print('POST', pos)
                if not pos:
                    request.env['siat.pos'].create({
                        'codigo_sucursal': sucursal,
                        'codigo': item['codigoPuntoVenta'],
                        'tipo_id': 1,
                        'tipo_descripcion': item['tipoPuntoVenta'],
                        'nombre': item['nombrePuntoVenta'],
                        'descripcion': '',
                        'direccion': '',
                        'ciudad': '',
                        'telefono': '',
                    })

            return request.make_json_response({
                'status': 'ok',
                'code': 200,
                'data': res
            })
        except Exception as e:
            return request.make_json_response({
                'status': 'error',
                'code': 500,
                'data': None,
                'error': str(e)
            })

    @http.route(['/siat/puntos-venta/<int:id>'], auth='user', type='http', methods=['DELETE'], csrf=False)
    def delete(self, **params):
        self._check_session()
        _id = params.get('id', 0)
        try:
            service = ServiceSiatOperations()
            res = service.borrar_puntoventa(_id)

            return request.make_json_response({
                'status': 'ok',
                'code': 200,
                'data': res
            })
        except Exception as e:
            return request.make_json_response({
                'status': 'error',
                'code': 200,
                'data': None,
                'error': str(e)
            })



