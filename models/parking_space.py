
from odoo import models, fields, api

class ParkingSpace(models.Model):
    _name = 'parking.space'
    _description = 'Parking Space Management'

    name = fields.Char(string='Parking Space', required=True)
    location = fields.Char(string='Location')
    type = fields.Selection([('shop', 'Shop'), ('visitor', 'Visitor')], string='Type', required=True)
    is_occupied = fields.Boolean(string='Occupied', default=False)
    allocated_to = fields.Many2one('shop.tenant', string='Allocated To', domain="[('is_shop_owner', '=', True)]")
    occupied_by = fields.Char(string='Occupied By')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    parking_fee = fields.Float(string='Parking Fee', compute='_compute_parking_fee')

    @api.depends('start_time', 'end_time')
    def _compute_parking_fee(self):
        fee_per_hour = 5  # Example fee rate
        for record in self:
            if record.start_time and record.end_time:
                duration = record.end_time - record.start_time
                hours = duration.total_seconds() / 3600
                record.parking_fee = fee_per_hour * hours
            else:
                record.parking_fee = 0.0

class ParkingTransaction(models.Model):
    _name = 'parking.transaction'
    _description = 'Parking Transaction'

    space_id = fields.Many2one('parking.space', string='Parking Space', required=True)
    tenant_id = fields.Many2one('shop.tenant', string='Tenant')
    occupied_by = fields.Char(string='Occupied By')
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    parking_fee = fields.Float(string='Parking Fee', related='space_id.parking_fee', store=True)
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], string='Status', default='ongoing')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.space_id:
            record.space_id.write({
                'is_occupied': True,
                'allocated_to': record.tenant_id.id,
                'occupied_by': record.occupied_by,
                'start_time': record.start_time,
                'end_time': record.end_time,
            })
        return record

    def end_parking(self):
        for record in self:
            record.state = 'completed'
            if record.space_id:
                record.space_id.write({
                    'is_occupied': False,
                    'allocated_to': False,
                    'occupied_by': False,
                    'start_time': False,
                    'end_time': False,
                })
