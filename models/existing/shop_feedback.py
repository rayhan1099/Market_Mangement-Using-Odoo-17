from odoo import models, fields, api

class ShopFeedback(models.Model):
    _name = 'shop.feedback'
    _description = 'Shop Feedback and Complaint Management'

    customer_name = fields.Char(string='Customer Name', required=True)
    shop_id = fields.Many2one('market.shop', string='Shop', required=True)
    feedback_type = fields.Selection([('feedback', 'Feedback'), ('complaint', 'Complaint')], string='Type', required=True)
    description = fields.Text(string='Description', required=True)
    resolution_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], string='Resolution Status', default='pending')
    resolution_notes = fields.Text(string='Resolution Notes')
    feedback_date = fields.Datetime(string='Feedback Date', default=fields.Datetime.now, required=True)
    rating = fields.Selection([
        ('1', '1 - Very Bad'),
        ('2', '2 - Bad'),
        ('3', '3 - Average'),
        ('4', '4 - Good'),
        ('5', '5 - Excellent')
    ], string='Rating')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.feedback_type == 'complaint' and record.resolution_status == 'resolved':
            self._update_shop_rating(record.shop_id)
        return record

    def write(self, vals):
        result = super().write(vals)
        for record in self:
            if record.feedback_type == 'complaint' and 'resolution_status' in vals and vals['resolution_status'] == 'resolved':
                self._update_shop_rating(record.shop_id)
        return result

    def _update_shop_rating(self, shop):
        feedbacks = self.search([('shop_id', '=', shop.id), ('feedback_type', '=', 'feedback'), ('rating', '!=', False)])
        total_rating = sum(int(feedback.rating) for feedback in feedbacks)
        shop.rating = total_rating / len(feedbacks) if feedbacks else 0

class MarketShop(models.Model):
    _inherit = 'market.shop'

    feedback_ids = fields.One2many('shop.feedback', 'shop_id', string='Feedbacks')
    rating = fields.Float(string='Average Rating', compute='_compute_rating', store=True)

    @api.depends('feedback_ids.rating')
    def _compute_rating(self):
        for shop in self:
            feedbacks = shop.feedback_ids.filtered(lambda f: f.feedback_type == 'feedback' and f.rating)
            if feedbacks:
                shop.rating = sum(int(f.rating) for f in feedbacks) / len(feedbacks)
            else:
                shop.rating = 0
