from odoo import models, fields, api


class ShopPerformance(models.Model):
    _name = 'shop.performance'
    _description = 'Shop Performance Monitoring'

    shop_id = fields.Many2one('market.shop', string='Shop', required=True)
    sales = fields.Float(string='Total Sales')
    area = fields.Float(string='Shop Area (sq ft)', related='shop_id.shopsize')
    sales_per_sqft = fields.Float(string='Sales per Square Foot', compute='_compute_sales_per_sqft', store=True)
    performance_date = fields.Date(string='Performance Date', required=True, default=fields.Date.today)

    @api.depends('sales', 'area')
    def _compute_sales_per_sqft(self):
        for record in self:
            if record.area:
                record.sales_per_sqft = record.sales / record.area
            else:
                record.sales_per_sqft = 0.0

    @api.model
    def create(self, vals):
        # Implement logic for automatic performance tracking
        res = super(ShopPerformance, self).create(vals)
        return res
