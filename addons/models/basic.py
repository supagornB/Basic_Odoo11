# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class Basic(models.Model):
    _name = 'basic'
    _description = "Basic Modue"
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, default=lambda self: _('New'))
    date = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='State', required=True, copy=False, index=True, default='draft')
    lines = fields.One2many('basic.line', 'basic_id', string='Basic Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('basic') or _('New')
        return super(Basic, self).create(vals)


class BasicLine(models.Model):
    _name = 'basic.line'
    _description = "Basic Line"

    basic_id = fields.Many2one('basic', string="Basic", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure')
    price_unit = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), default=0.0)
    amount = fields.Float(string='Amount', readonly=True)

    @api.multi
    @api.onchange('product_id')
    def onchange_product(self):
        product = self.product_id
        self.product_uom = product.uom_id
        self.price_unit = product.lst_price
        self.onchange_uom_qty()

    @api.multi
    @api.onchange('product_uom_qty','price_unit')
    def onchange_uom_qty(self):
        amount = self.product_uom_qty * self.price_unit
        self.amount = amount
