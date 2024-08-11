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
        ('cleaning', 'Cleaning'),
    ], string='Staff Category', required=True)

    # Common fields
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string='Email')
    staff_salary = fields.Float(string='Salary')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    # Security specific fields
    security_license_number = fields.Char(string='Security License Number')
    shift_hours = fields.Char(string='Shift Hours')

    # Maintenance specific fields
    maintenance_skills = fields.Text(string='Skills')
    certification_number = fields.Char(string='Certification Number')

    # Admin specific fields
    department = fields.Char(string='Department')
    office_location = fields.Char(string='Office Location')

    # Sales specific fields
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
        staff_category_fields = {
            'security': ['security_license_number', 'shift_hours'],
            'maintenance': ['maintenance_skills', 'certification_number'],
            'admin': ['department', 'office_location'],
            'sales': ['campaigns_managed', 'marketing_skills'],
            'cleaning': ['cleaning_schedule', 'equipment_handled'],
        }

        # Get the fields to be shown for the selected category
        fields_to_show = staff_category_fields.get(self.staff_category, [])

        # Clear all fields first
        for field in staff_category_fields.values():
            for field_name in field:
                setattr(self, field_name, False)

        # Show fields specific to the selected category
        return {
            'fields': {
                field: {'required': True} for field in fields_to_show
            }
        }
