from odoo import models, fields, api

class MarketSecurity(models.Model):
    _name = 'market.security'
    _description = 'Market Security Management'

    name = fields.Char(string='Name', required=True)
    personnel_ids = fields.One2many('market.security.personnel', 'security_id', string='Security Personnel')
    schedule_ids = fields.One2many('market.security.schedule', 'security_id', string='Schedules')
    incident_ids = fields.One2many('market.security.incident', 'security_id', string='Incidents')
    cctv_monitoring = fields.Boolean(string='CCTV Monitoring', default=False)

class MarketSecurityPersonnel(models.Model):
    _name = 'market.security.personnel'
    _description = 'Market Security Personnel'

    name = fields.Char(string='Name', required=True)
    security_id = fields.Many2one('market.security', string='Security Management')
    assignment = fields.Char(string='Assignment')
    contact_info = fields.Char(string='Contact Information')

class MarketSecuritySchedule(models.Model):
    _name = 'market.security.schedule'
    _description = 'Market Security Schedule'

    security_id = fields.Many2one('market.security', string='Security Management')
    personnel_id = fields.Many2one('market.security.personnel', string='Personnel')
    shift_start = fields.Datetime(string='Shift Start')
    shift_end = fields.Datetime(string='Shift End')

class MarketSecurityIncident(models.Model):
    _name = 'market.security.incident'
    _description = 'Market Security Incident'

    security_id = fields.Many2one('market.security', string='Security Management')
    incident_date = fields.Datetime(string='Incident Date')
    description = fields.Text(string='Description')
    response = fields.Text(string='Response')
