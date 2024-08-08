from odoo import models, fields, api

class MarketUtilityBill(models.Model):
    _name = 'market.utility.bill'
    _description = 'Utility Bill Management'

    shop_id = fields.Many2one('market.shop', string='Shop', required=True)
    billing_date = fields.Date(string='Billing Date', required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Payment Status', default='unpaid')
    utility_ids = fields.One2many('market.utility', 'bill_id', string='Utilities')

    @api.depends('utility_ids.amount_due')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(utility.amount_due for utility in record.utility_ids)
