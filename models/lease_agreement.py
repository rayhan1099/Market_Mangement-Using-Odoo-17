from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
import base64
import io
from PyPDF2 import PdfFileReader




class LeaseAgreement(models.Model):
    _name = 'lease.agreement'
    _description = 'Lease Agreement Management'

    name = fields.Char(string='Lease Agreement Name', required=True)
    tenant_id = fields.Many2one('shop.tenant', string='Tenant', required=True)
    shop_id = fields.Many2one('market.shop', string='Shop', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    digital_copy = fields.Binary(string='Digital Copy', attachment=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated')
    ], string='Status', default='active', compute='_compute_state', store=True)
    reminder_date = fields.Date(string='Reminder Date', compute='_compute_reminder_date', store=True)

    @api.depends('end_date')
    def _compute_state(self):
        today = fields.Date.today()
        for record in self:
            if record.end_date and record.end_date < today:
                record.state = 'expired'
            elif record.state != 'terminated':
                record.state = 'active'

    @api.depends('end_date', 'state')
    def _compute_reminder_date(self):
        for record in self:
            if record.end_date:
                reminder_period = timedelta(days=5)  # Reminder period before lease end date
                record.reminder_date = record.end_date - reminder_period

    @api.model
    def send_lease_reminders(self):
        today = fields.Date.today()
        agreements = self.search([('reminder_date', '=', today), ('state', '=', 'active')])
        for agreement in agreements:
            template = self.env.ref('your_module.lease_reminder_email_template')
            if template:
                template.send_mail(agreement.id, force_send=True)
            else:
                _logger.error("Lease reminder email template not found.")


