# -*- coding: utf-8 -*-

import base64
import logging

from odoo import _, api, fields, models, tools, Command
from odoo.exceptions import UserError
from odoo.tools import is_html_empty

_logger = logging.getLogger(__name__)


class SiatMailTemplate(models.Model):
    _inherit = 'mail.template'
    append_attachments = []

    def generate_email(self, res_ids, fields):
        res = super(SiatMailTemplate, self).generate_email(res_ids, fields)
        if self.model != 'siat.invoice':
            return res

        print('APPEND ATTACHMENTS TO EMAIL')
        # print('APPEND ATTACHMENTS', self.append_attachments)
        for attach in SiatMailTemplate.append_attachments:
            res['attachments'].append( attach )

        # print(res)

        return res

