from odoo import models, fields, api

class Shop(models.Model):
    _name = 'market.shop'
    _description = 'Shop Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='Shop No', required=True, unique=True)
    rent_per_sq = fields.Float(string='Rent Per SQ Feet', required=True)
    rent = fields.Float(string='Rent', compute='_compute_rent', store=True)
    state = fields.Selection([('available', 'Available'), ('unavailable', 'Unavailable')], default='available')
    market_id = fields.Many2one('market.market', string='Market')
    floor = fields.Selection([
        ('1', 'Floor 1'),
        ('2', 'Floor 2'),
        ('3', 'Floor 3'),
        ('4', 'Floor 4'),
        ('5', 'Floor 5'),
    ], string='Floor', required=True)
    blocks = fields.Selection([
        ('A', 'Block A'),
        ('B', 'Block B'),
        ('C', 'Block C'),
        ('D', 'Block D'),
    ], string='Block', required=True)
    shopsize = fields.Float(string='Shop Size (sq. ft)', required=True)
    owner_ids = fields.One2many('shop.tenant', 'shop_id', string='Owners')
    current_owner_id = fields.Many2one('shop.tenant', string='Current Owner', compute='_compute_current_owner', store=True)
    rent_end_date = fields.Date(string='Rent End Date')

    _sql_constraints = [
        ('unique_shop_name', 'unique(name)', 'The Shop No must be unique.')
    ]

    @api.depends('shopsize', 'rent_per_sq')
    def _compute_rent(self):
        for shop in self:
            shop.rent = shop.shopsize * shop.rent_per_sq

    @api.onchange('shopsize', 'rent_per_sq')
    def _onchange_shopsize(self):
        if self.shopsize and self.rent_per_sq:
            self.rent = self.shopsize * self.rent_per_sq

    @api.depends('owner_ids')
    def _compute_current_owner(self):
        for shop in self:
            if shop.state == 'available':
                shop.current_owner_id = False
            else:
                shop.current_owner_id = shop.owner_ids.sorted('rent_start_date', reverse=True)[:1] if shop.owner_ids else False

    def update_shop_state(self):
        today = fields.Date.today()
        for shop in self.search([('state', '=', 'unavailable')]):
            if shop.rent_end_date and shop.rent_end_date <= today:
                shop.write({'state': 'available'})
