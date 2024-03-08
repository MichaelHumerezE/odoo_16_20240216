# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
import json

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_siat_pos_id = fields.Many2one(
        'siat.pos',
        related='pos_config_id.siat_pos_id',
        readonly=False,
        # precompute=False,
        # default='0'
    )

    '''
    def _get_modalidades(self):
        return [
            ('0', '-- modalidad --'),
            ('1', 'Electronica'),
            ('2', 'Computarizada')
        ]

    def _get_ambientes(self):
        return [
            ('0', '-- ambiente --'),
            ('1', 'Produccion'),
            ('2', 'Piloto/Pruebas')
        ]
    
    @api.depends('siat_config')
    def _compute_nombre_sistema(self):
        pass

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        print('SET VALUES', res)
        print('siat_config', self.siat_config)
        print('nombre_sistema', self.nombre_sistema)
        print('codigo_sistema', self.codigo_sistema)
        print('self.nit', self.nit)

        self.env['ir.config_parameter'].set_param('siat_config.siat_config', self.siat_config)
        return res
    '''

    # def get_values(self):
    #    print('COMPANY', self.env.company)

    #    res = super(ResConfigSettings, self).get_values()
        # print('GET VALUES', res)
    #    value = self.env['ir.config_parameter'].sudo().get_param('siat_config.siat_config')
    #    data = {
    #        'siat_config': value,
    #        'nombre_sistema': '',
    #        'codigo_sistema': '',
    #        'nit': '',
    #        'razon_social': '',
    #        'token_delegado': '',
    #        'modalidad': 0,
    #        'ambiente': 0,
    #    }
    #    try:
    #        config = json.loads(value)
    #        if value and type(config) is dict:
    #            data.update(config)
    #    except:
    #        pass

    #    res.update(data)
    #    print('GET VALUES', res)
    #    '''
    #    for key in ['siat_config', 'nombre_sistema', 'codigo_sistema', 'nit']:
    #        value = self.env['ir.config_parameter'].sudo().get_param(key)
    #        svalue = self.env['ir.config_parameter'].sudo().get_param('siat_config.' + key)
    #        print(key + ' VALUE: ', value, svalue)
    #        res.update(key=key)
    #    '''
    #    '''
    #    config = self.search([('company_id', '=', self.env.company.id)], order='id DESC', limit=1)
    #    print('CONFIG', config)
    #    if len(config) > 0 and config.siat_config:
    #        data = json.loads(config.siat_config)
    #        print('DATA', data)
    #        res.update(data or {})
    #    '''
    #    return res

