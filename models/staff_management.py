from odoo import models, fields, api


class StaffManagement(models.Model):
    _name = 'staff.management'
    _description = 'Staff Management'

    name = fields.Char(string='Staff Name', required=True)
    market_id = fields.Many2one('market.market', string='Market', required=True)
    staff_category = fields.Selection([
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
        ('admin', 'Administration'),
        ('sales', 'Sales'),
        ('cleaning', 'Cleaning')
    ], string='Staff Category', required=True)

    staff_type = fields.Selection([
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
        ('admin', 'Admin'),
        ('marketing', 'Marketing'),
        ('cleaning', 'Cleaning')
    ], string='Staff Type', required=True)

    # Common fields
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string='Email')
    staff_salary = fields.Float(string='Salary')
    schedule = fields.Datetime(string='Schedule')

    # Security specific fields
    security_license_number = fields.Char(string='Security License Number')
    shift_hours = fields.Char(string='Shift Hours')

    # Maintenance specific fields
    maintenance_skills = fields.Text(string='Skills')
    certification_number = fields.Char(string='Certification Number')

    # Admin specific fields
    department = fields.Char(string='Department')
    office_location = fields.Char(string='Office Location')

    # Marketing specific fields
    campaigns_managed = fields.Integer(string='Number of Campaigns Managed')
    marketing_skills = fields.Text(string='Marketing Skills')

    # Cleaning specific fields
    cleaning_schedule = fields.Char(string='Cleaning Schedule')
    equipment_handled = fields.Text(string='Equipment Handled')

    total_staff = fields.Integer(string='Total Staff', compute='_compute_total_staff')

    @api.depends('market_id', 'staff_category')
    def _compute_total_staff(self):
        for record in self:
            record.total_staff = self.search_count([
                ('market_id', '=', record.market_id.id),
                ('staff_category', '=', record.staff_category)
            ])

    @api.onchange('staff_category')
    def _onchange_staff_category(self):
        staff_type_options = {
            'security': [('security', 'Security')],
            'maintenance': [('maintenance', 'Maintenance')],
            'admin': [('admin', 'Admin')],
            'sales': [('marketing', 'Marketing')],
            'cleaning': [('cleaning', 'Cleaning')]
        }
        self.staff_type = False
        return {'domain': {'staff_type': staff_type_options.get(self.staff_category, [])}}

    @api.onchange('staff_type')
    def _onchange_staff_type(self):
        # Clear fields that are not relevant for the selected staff type
        if self.staff_type == 'security':
            self._clear_fields_except(['security_license_number', 'shift_hours'])
        elif self.staff_type == 'maintenance':
            self._clear_fields_except(['maintenance_skills', 'certification_number'])
        elif self.staff_type == 'admin':
            self._clear_fields_except(['department', 'office_location'])
        elif self.staff_type == 'marketing':
            self._clear_fields_except(['campaigns_managed', 'marketing_skills'])
        elif self.staff_type == 'cleaning':
            self._clear_fields_except(['cleaning_schedule', 'equipment_handled'])

    def _clear_fields_except(self, allowed_fields):
        # List of all specific fields
        all_fields = [
            'security_license_number', 'shift_hours',
            'maintenance_skills', 'certification_number',
            'department', 'office_location',
            'campaigns_managed', 'marketing_skills',
            'cleaning_schedule', 'equipment_handled'
        ]
        for field in all_fields:
            if field not in allowed_fields:
                setattr(self, field, False)
