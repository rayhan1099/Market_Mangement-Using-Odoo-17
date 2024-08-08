from odoo import models, fields, api

class MarketMaintenance(models.Model):
    _name = 'market.maintenance'
    _description = 'Market Maintenance Management'

    name = fields.Char(string='Request Name', required=True)
    tenant_id = fields.Many2one('shop.tenant', string='Tenant', required=True)
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today, required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)
    repair_job_ids = fields.One2many('market.maintenance.repair', 'maintenance_id', string='Repair Jobs')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost')

    @api.depends('repair_job_ids.cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(job.cost for job in record.repair_job_ids)

class MarketMaintenanceRepair(models.Model):
    _name = 'market.maintenance.repair'
    _description = 'Market Maintenance Repair Job'

    name = fields.Char(string='Repair Job', required=True)
    maintenance_id = fields.Many2one('market.maintenance', string='Maintenance Request', required=True)
    job_date = fields.Date(string='Job Date', required=True)
    description = fields.Text(string='Description')
    cost = fields.Float(string='Cost')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Status', default='pending', required=True)
