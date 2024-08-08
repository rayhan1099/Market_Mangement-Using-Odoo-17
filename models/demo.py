# @api.model
# def create(self, vals):
#     shop = self.env['market.shop'].browse(vals['shop_id'])
#     if shop.state == 'available':
#         # Check if there is any other owner history linked to the shop
#         existing_owner_history = self.env['owner.history'].search([('shop_id', '=', shop.id)])
#         if not existing_owner_history:
#             shop.write({'state': 'unavailable'})
#     else:
#         raise UserError("The selected shop is unavailable.")
#
#     return super(ShopOwnerHistory, self).create(vals)
#
# def unlink(self):
#     for record in self:
#         shop = record.shop_id
#         # Check if the shop has no other owners
#         remaining_owners = self.env['owner.history'].search([('shop_id', '=', shop.id)])
#         if not remaining_owners:
#             shop.write({'state': 'available'})
#     return super(ShopOwnerHistory, self).unlink()
#
# # @api.model
# # def _auto_revert_shop_state(self):
# #     today = date.today()
# #     expired_rent_histories = self.env['owner.history'].search([('rent_end_date', '<', today), ('shop_id.state', '=', 'unavailable')])
# #     for history in expired_rent_histories:
# #         shop = history.shop_id
# #         shop.write({'state': 'available'})