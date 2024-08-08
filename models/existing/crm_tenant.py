from odoo import models, fields, api

class CrmTenant(models.Model):
    _name = 'crm.tenant'
    _description = 'Tenant CRM Management'

    name = fields.Char(string='Tenant Name', required=True)
    contact_details = fields.Char(string='Contact Details')
    potential = fields.Boolean(string='Potential Tenant')
    current = fields.Boolean(string='Current Tenant')
    communication_history_ids = fields.One2many('crm.communication.history', 'tenant_id', string='Communication History')
    follow_up_task_ids = fields.One2many('crm.follow.up.task', 'tenant_id', string='Follow-up Tasks')
    marketing_automation_ids = fields.One2many('crm.marketing.automation', 'tenant_id', string='Marketing Automation')

class CrmCommunicationHistory(models.Model):
    _name = 'crm.communication.history'
    _description = 'Communication History'

    tenant_id = fields.Many2one('crm.tenant', string='Tenant')
    communication_date = fields.Datetime(string='Communication Date', default=fields.Datetime.now)
    communication_type = fields.Selection([
        ('email', 'Email'),
        ('call', 'Call'),
        ('meeting', 'Meeting')
    ], string='Type', required=True)
    notes = fields.Text(string='Notes')

class CrmFollowUpTask(models.Model):
    _name = 'crm.follow.up.task'
    _description = 'Follow-up Tasks'

    tenant_id = fields.Many2one('crm.tenant', string='Tenant')
    task_date = fields.Datetime(string='Task Date', default=fields.Datetime.now)
    task_description = fields.Text(string='Task Description')
    completed = fields.Boolean(string='Completed')

class CrmMarketingAutomation(models.Model):
    _name = 'crm.marketing.automation'
    _description = 'Marketing Automation'

    tenant_id = fields.Many2one('crm.tenant', string='Tenant')
    campaign_name = fields.Char(string='Campaign Name')
    campaign_date = fields.Datetime(string='Campaign Date', default=fields.Datetime.now)
    campaign_details = fields.Text(string='Campaign Details')
    response_received = fields.Boolean(string='Response Received')
