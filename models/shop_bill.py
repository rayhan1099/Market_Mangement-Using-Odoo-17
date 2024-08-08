from odoo import models, fields, api

class ShopBill(models.Model):
    _name = 'shop.bill'
    _description = 'Shop Bill'

    shop_id = fields.Many2one('market.shop', string="Shop No")
    rent = fields.Float(related='shop_id.rent', string="Rent", store=True, readonly=True)
    electricity_bill_per_sq = fields.Float(string='Electricity Bill Per Sq Ft')
    total_electricity_bill = fields.Float(string='Total Electricity Bill', compute='_compute_total_electricity')
    service_charge_per_sq = fields.Float(string='Service Charge Per Sq Ft')
    service_charge = fields.Float(string='Service Charge (Other Charge)', compute='_compute_service_charge')
    total_bill = fields.Float(string="Total Bill", compute='_compute_total_bill')

    @api.depends('shop_id.shopsize', 'electricity_bill_per_sq')
    def _compute_total_electricity(self):
        for record in self:
            record.total_electricity_bill = record.shop_id.shopsize * record.electricity_bill_per_sq

    @api.depends('shop_id.shopsize', 'service_charge_per_sq')
    def _compute_service_charge(self):
        for record in self:
            record.service_charge = record.shop_id.shopsize * record.service_charge_per_sq

    @api.depends('rent', 'total_electricity_bill', 'service_charge')
    def _compute_total_bill(self):
        for record in self:
            record.total_bill = record.rent + record.total_electricity_bill + record.service_charge
