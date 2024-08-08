from odoo import models, fields, api

class MarketEvent(models.Model):
    _name = 'market.event'
    _description = 'Market Event Management'

    name = fields.Char(string='Event Name', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    description = fields.Text(string='Description')
    shop_ids = fields.Many2many('market.shop', string='Shops Involved')
    attendance_count = fields.Integer(string='Attendance Count', compute='_compute_attendance_count')
    event_type = fields.Selection([
        ('promotion', 'Promotion'),
        ('event', 'Event'),
    ], string='Event Type', required=True)
    impact_on_sales = fields.Float(string='Impact on Sales', compute='_compute_impact_on_sales')
    foot_traffic_increase = fields.Float(string='Foot Traffic Increase', compute='_compute_foot_traffic_increase')

    @api.depends('shop_ids')
    def _compute_attendance_count(self):
        for event in self:
            # Placeholder logic for calculating attendance count
            event.attendance_count = len(event.shop_ids) * 10

    @api.depends('shop_ids.sales')
    def _compute_impact_on_sales(self):
        for event in self:
            total_sales = sum(shop.sales for shop in event.shop_ids)
            event.impact_on_sales = total_sales * 0.1  # Placeholder for impact calculation

    @api.depends('shop_ids.foot_traffic')
    def _compute_foot_traffic_increase(self):
        for event in self:
            total_traffic = sum(shop.foot_traffic for shop in event.shop_ids)
            event.foot_traffic_increase = total_traffic * 0.2  # Placeholder for foot traffic increase calculation
