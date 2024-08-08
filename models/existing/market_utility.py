from odoo import models, fields, api

class MarketUtility(models.Model):
    _name = 'market.utility'
    _description = 'Utility Management'

    shop_id = fields.Many2one('market.shop', string='Shop', required=True)
    utility_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('internet', 'Internet')
    ], string='Utility Type', required=True)
    consumption = fields.Float(string='Consumption', required=True)
    unit = fields.Selection([
        ('kwh', 'kWh'),  # for electricity
        ('m3', 'm³'),   # for water
        ('gb', 'GB')    # for internet
    ], string='Unit', required=True)
    billing_date = fields.Date(string='Billing Date', required=True)
    amount_due = fields.Float(string='Amount Due', compute='_compute_amount_due', store=True)
    bill_id = fields.Many2one('market.utility.bill', string='Utility Bill')

    @api.depends('consumption', 'utility_type')
    def _compute_amount_due(self):
        for record in self:
            if record.utility_type == 'electricity':
                rate = 0.1  # example rate per kWh
            elif record.utility_type == 'water':
                rate = 1.5  # example rate per m³
            elif record.utility_type == 'internet':
                rate = 10  # example rate per GB
            else:
                rate = 0
            record.amount_due = record.consumption * rate

