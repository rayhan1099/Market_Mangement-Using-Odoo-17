
from odoo import models, fields, api

class FinancialReporting(models.Model):
    _name = 'financial.reporting'
    _description = 'Financial Reporting and Analytics'

    name = fields.Char(string='Report Name', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    total_revenue = fields.Float(string='Total Revenue', compute='_compute_total_revenue')
    total_expenses = fields.Float(string='Total Expenses', compute='_compute_total_expenses')
    profit_margin = fields.Float(string='Profit Margin', compute='_compute_profit_margin')
    revenue_expenses_report = fields.Text(string='Revenue and Expenses Report', compute='_compute_revenue_expenses_report')

    @api.depends('start_date', 'end_date')
    def _compute_total_revenue(self):
        for report in self:
            # Calculate total revenue for the given date range
            revenue = self.env['market.shop'].search([
                ('date', '>=', report.start_date),
                ('date', '<=', report.end_date),
                ('state', '=', 'available')
            ]).mapped('rent')
            report.total_revenue = sum(revenue)

    @api.depends('start_date', 'end_date')
    def _compute_total_expenses(self):
        for report in self:
            # Calculate total expenses, including staff bills
            expenses = self.env['staff.management'].search([
                ('staff_type', '!=', False)
            ]).mapped('staff_bills')
            report.total_expenses = sum(expenses)

    @api.depends('total_revenue', 'total_expenses')
    def _compute_profit_margin(self):
        for report in self:
            if report.total_revenue:
                report.profit_margin = ((report.total_revenue - report.total_expenses) / report.total_revenue) * 100
            else:
                report.profit_margin = 0

    @api.depends('start_date', 'end_date')
    def _compute_revenue_expenses_report(self):
        for report in self:
            revenue_expenses = f"Total Revenue: {report.total_revenue}\nTotal Expenses: {report.total_expenses}\nProfit Margin: {report.profit_margin}%"
            report.revenue_expenses_report = revenue_expenses
