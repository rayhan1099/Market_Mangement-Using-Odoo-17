from odoo import models, fields, api


class Shop(models.Model):
    _name = 'market.shop'
    _description = 'Shop Management'
    name = fields.Char(string='Shop No', required=True, unique=True)
    rent = fields.Float(string='Rent', compute='_compute_rent', store=True)
    state = fields.Selection([('available', 'Available'), ('unavailable', 'Unavailable')], default='available')
    market_id = fields.Many2one('market.market', string='Market')
    floor = fields.Selection([
        ('1', 'Floor 1'),
        ('2', 'Floor 2'),
        ('3', 'Floor 3'),
        ('4', 'Floor 4'),
        ('5', 'Floor 5'),
        # Add more floors as needed
    ], string='Floor', required=True)
    blocks = fields.Selection([  # Change 'blocks' to 'block'
        ('A', 'Block A'),
        ('B', 'Block B'),
        ('C', 'Block C'),
        ('D', 'Block D'),
        # Add more blocks as needed
    ], string='Block', required=True)

    shopsize = fields.Float(string='Shop Size (sq. ft)', required=True)

    _sql_constraints = [
        ('unique_shop_name', 'unique(name)', 'The Shop No must be unique.')
    ]

    @api.depends('shopsize')
    def _compute_rent(self):
        rate_per_square_feet = 100  # Assuming the rate per square foot is 100
        for shop in self:
            shop.rent = shop.shopsize * rate_per_square_feet

    @api.onchange('shopsize')
    def _onchange_shopsize(self):
        if self.shopsize:
            rate_per_square_feet = 100  # Assuming the rate per square foot is 100
            self.rent = self.shopsize * rate_per_square_feet
