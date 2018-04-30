# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class Basic(models.Model):
    _name = 'basic'
    _description = "Basic Modue"
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    date = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='State', required=True, copy=False, index=True, default='draft')
    lines = fields.One2many('basic.line', 'basic_id', string='Basic Lines')


class BasicLine(models.Model):
    _name = 'basic.line'
    _description = "Basic Line"

    basic_id = fields.Many2one('basic', string="Basic", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure')
    price_unit = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), default=0.0)
    amount = fields.Float(string='Amount', readonly=True)
