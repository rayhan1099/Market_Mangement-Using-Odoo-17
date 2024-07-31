from odoo import models, fields, api

class MarketMarket(models.Model):
    _name = 'market.market'
    _description = 'Market Management'

    name = fields.Char(string='Market Name', required=True)
    total_shops = fields.Integer(string='Total Shops', compute='_compute_total_shops')
    shop_ids = fields.One2many('market.shop', 'market_id', string='Shops')
    total_floors = fields.Integer(string='Total Floors', compute='_compute_total_floors')
    available_shops = fields.Integer(string='Available Shops', compute='_compute_shop_availability')
    unavailable_shops = fields.Integer(string='Unavailable Shops', compute='_compute_shop_availability')
    total_shops_per_floor = fields.Text(string='Total Shops Per Floor', compute='_compute_total_shops_per_floor')
    total_shops_by_block = fields.Text(string='Total Shops By Block', compute='_compute_total_shops_by_block')

    @api.depends('shop_ids')
    def _compute_total_shops_per_floor(self):
        for market in self:
            floor_counts = {}
            for shop in market.shop_ids:
                if shop.floor not in floor_counts:
                    floor_counts[shop.floor] = 0
                floor_counts[shop.floor] += 1
            market.total_shops_per_floor = ', '.join(
                f'Floor {floor}: {count} shops' for floor, count in floor_counts.items())

    @api.depends('shop_ids')
    def _compute_total_shops(self):
        for record in self:
            record.total_shops = len(record.shop_ids)

    @api.depends('shop_ids')
    def _compute_shop_availability(self):
        for record in self:
            available = len(record.shop_ids.filtered(lambda s: s.state == 'available'))
            record.available_shops = available
            record.unavailable_shops = record.total_shops - available

    def _compute_total_floors(self):
        for market in self:
            floors = set()
            for shop in market.shop_ids:
                if shop.floor:
                    floors.add(shop.floor)
            market.total_floors = len(floors)
    @api.depends('shop_ids')
    def _compute_total_shops_by_block(self):
        for market in self:
            block_counts = {}
            for shop in market.shop_ids:
                if shop.blocks not in block_counts:
                    block_counts[shop.blocks] = 0
                block_counts[shop.blocks] += 1
            market.total_shops_by_block = ', '.join(
                f'Block {block}: {count} shops' for block, count in block_counts.items())
