from odoo import models, fields, api
from odoo.exceptions import UserError

class ParkingSpace(models.Model):
    _name = 'parking.space'
    _description = 'Parking Space'

    name = fields.Char(string='Parking Space', required=True)
    location = fields.Char(string='Location')
    is_occupied = fields.Boolean(string='Is Occupied', default=False)
    allocated_to = fields.Many2one('shop.tenant', string='Allocated To')
    occupied_by = fields.Char(string='Occupied By', readonly="True")
    start_time = fields.Datetime(string='Start Time', readonly="True")
    end_time = fields.Datetime(string='End Time', readonly="True")
    license_plate = fields.Char(string='License Plate', readonly="True")
    security_camera_id = fields.Many2one('security.camera', string='Security Camera')

    def release_parking_space(self):
        for record in self:
            record.write({
                'is_occupied': False,
                'allocated_to': False,
                'occupied_by': False,
                'start_time': False,
                'end_time': False,
                'license_plate': False,
            })

class ParkingTransaction(models.Model):
    _name = 'parking.transaction'
    _description = 'Parking Transaction'

    space_id = fields.Many2one('parking.space', string='Parking Space', required=True)
    tenant_id = fields.Many2one('shop.tenant', string='Tenant')
    occupied_by = fields.Char(string='Occupied By')
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    parking_fee = fields.Float(string='Parking Fee', compute='_compute_parking_fee', store=True)
    license_plate = fields.Char(string='License Plate')
    reservation_priority = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], string='Reservation Priority')
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], string='Status', default='ongoing')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('mobile_payment', 'Mobile Payment')
    ], string='Payment Method', required=True)
    transaction_reference_number = fields.Char(string='Transaction Reference Number', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        vals['transaction_reference_number'] = self.env['ir.sequence'].next_by_code('parking.transaction') or '/'
        record = super(ParkingTransaction, self).create(vals)
        if record.space_id:
            record.space_id.write({
                'is_occupied': True,
                'allocated_to': record.tenant_id.id,
                'occupied_by': record.occupied_by,
                'start_time': record.start_time,
                'end_time': record.end_time,
                'license_plate': record.license_plate,
            })
        return record

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

    def end_parking(self):
        for record in self:
            record.state = 'completed'
            if record.space_id:
                record.space_id.release_parking_space()

    def process_payment(self):
        for record in self:
            if not record.parking_fee:
                raise UserError('Parking fee has not been calculated.')
            # Implement contactless payment logic here
            print(f"Processed {record.parking_fee} payment via {record.payment_method} for license plate {record.license_plate}.")

class SecurityCamera(models.Model):
    _name = 'security.camera'
    _description = 'Security Camera'

    name = fields.Char(string='Camera Name', required=True)
    location = fields.Char(string='Location')
    monitored_spaces = fields.One2many('parking.space', 'security_camera_id', string='Monitored Spaces')

    def monitor_parking_space(self, space_id):
        space = self.env['parking.space'].browse(space_id)
        # Implement the logic to monitor the parking space via the security camera
        print(f"Monitoring parking space {space.name} using camera {self.name}.")
