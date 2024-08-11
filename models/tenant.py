from odoo import models, fields, api
from odoo.exceptions import UserError

class ShopTenant(models.Model):
    _name = 'shop.tenant'
    _description = 'Shop Tenant Information'

    shop_id = fields.Many2one('market.shop', string='Shop', required=True, domain=[('state', '=', 'available')])
    tenant_id = fields.Many2one('res.partner', string='Tenant', required=True)
    rent_start_date = fields.Date(string='Rent Start Date', required=True)
    rent_end_date = fields.Date(string='Rent End Date', required=True)
    shop_rent = fields.Float(string='Shop Rent', related='shop_id.rent', readonly=True)
    is_shop_owner = fields.Boolean(string='Is Shop Owner', default=False)

    @api.model
    def create(self, vals):
        shop = self.env['market.shop'].browse(vals['shop_id'])
        if shop.state != 'available':
            raise UserError('The selected shop is not available.')
        shop.write({'state': 'unavailable'})
        return super(ShopTenant, self).create(vals)

    def unlink(self):
        for record in self:
            shop = record.shop_id
            # Check if the shop has no other tenants
            other_tenants = self.search([('shop_id', '=', shop.id), ('id', '!=', record.id)])
            if not other_tenants:
                shop.write({'state': 'available'})
        return super(ShopTenant, self).unlink()
