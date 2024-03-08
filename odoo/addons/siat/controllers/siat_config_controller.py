# -*- coding: utf-8 -*-
import os
import traceback
import logging
from odoo import http, _
from odoo.http import request, Controller
import json
from .siat_controller import SiatController
from .. import constants

_logger = logging.getLogger(__name__)


class SiatConfigController(Controller, SiatController):

    @http.route('/siat/config', type='http', auth='user', methods=['POST'], csrf=False)
    def save(self):
        self._check_session()
        try:

            if request.env.company.id is None:
                raise Exception('Identificador de compañia invalido')

            data = json.loads(request.httprequest.data)
            config = request.env['siat.config'].search([('company_id', '=', request.env.company.id)])
            if len(config) > 0:
                data['company_id'] = request.env.company.id
                if data['cafc'] is not None:
                    data['cafc'] = json.dumps(data['cafc'])

                config[0].write(data)
            else:
                config = request.env['siat.config'].create({**data, 'company_id': request.env.company.id})

            return request.make_json_response({'status': 'ok', 'code': 200, 'data': config.read()[0]})
        except Exception as e:
            print(traceback.print_exc())
            code = 500
            return request.make_json_response({
                'status': 'error',
                'code': code,
                'data': None,
                'error': str(e)
            }, status=code)

    @http.route('/siat/config', type='http', auth='user', methods=['GET'])
    def read(self):
        self._check_session()
        config = request.env['siat.config'].search([('company_id', '=', request.env.company.id)])
        company_dir = constants.DATA_DIR + '/cid-{0}'.format(request.env.company.id)
        if os.path.isdir(company_dir):
            cert_file = '{0}/certificado.pem'.format(company_dir)
            priv_file = '{0}/llave_privada.pem'.format(company_dir)
            if os.path.isfile(cert_file):
                config[0].pub_cert = 'certificado.pem';
            if os.path.isfile(priv_file):
                config[0].priv_cert = 'llave_privada.pem';

        return request.make_json_response({
            'status': 'ok',
            'code': 200,
            'data': config.read()[0] if len(config) > 0 else None
        })

    @http.route('/siat/config/certs', type='http', auth='user', methods=['POST'], csrf=False)
    def upload(self, redirect=None, **post):
        self._check_session()
        # print(post)
        company_dir = constants.DATA_DIR + '/cid-{0}'.format(request.env.company.id)
        if os.path.isdir(company_dir) is False:
            os.mkdir(company_dir)

        if post.get('cert') is not None:
            cert = post.get('cert')
            # print(cert.filename)
            # print(cert.read())
            filename = '{0}/certificado.pem'.format(company_dir)
            with open(filename, 'wb') as fout:
                fout.write(cert.read())

        if post.get('private_key') is not None:
            key = post.get('private_key')
            # print(cert.filename)
            # print(cert.read())
            filename = '{0}/llave_privada.pem'.format(company_dir)
            with open(filename, 'wb') as fout:
                fout.write(key.read())

        return request.make_json_response({
            'status': 'ok',
            'code': 200,
            'data': None,
            'message': 'Firma digital guardada correctamente.'
        })
