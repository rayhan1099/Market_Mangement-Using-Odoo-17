# from odoo import models, fields, api
# from odoo.exceptions import UserError
#
#
# class ShopOwner(models.Model):
#     _name = 'shop.owner'
#     _description = 'Shop Owner Information'
#
#     name = fields.Char(string='Name', required=True)
#     nid = fields.Char(string='National ID (NID)', required=True)
#     phone = fields.Char(string='Phone Number', required=True)
#     address = fields.Char(string='Address')
#     profession = fields.Char(string='Profession')
#     shop_id = fields.Many2one('market.shop', string='Shop', required=True)
#     start_date = fields.Date(string='Start Date', default=fields.Date.today)
#     end_date = fields.Date(string='End Date')
#
#     @api.model
#     def create(self, vals):
#         shop = self.env['market.shop'].browse(vals['shop_id'])
#         if shop.state == 'available':
#             shop.write({'state': 'unavailable'})
#         return super(ShopOwner, self).create(vals)
#
#     def unlink(self):
#         for record in self:
#             shop = record.shop_id
#             # Check if the shop has no other owners
#             if not shop.shop_owner_ids - record:
#                 shop.write({'state': 'available'})
#         return super(ShopOwner, self).unlink()
