import ast

import datetime as datetime

from odoo import api, fields, models, _


# Inherit project task model and make modify
class ProjectTask(models.Model):
    # _name = 'new_module.new_module'
    _inherit = 'project.task'

    # name = fields.Char()
    quantity = fields.Integer(string='Quantity', required=False)
    eco_type = fields.Many2one('sale.order', string='Related CEO', required=False)
    eco_type2 = fields.Many2one('mrp.eco', string='Related CEO', required=False)
    project_type = fields.Many2one('project.type', string='Project Type', required=False)
    is_sample_order = fields.Boolean(string='Is Sample Order')
    is_procurement = fields.Boolean(string='Is Procurement')
    is_plm = fields.Boolean(string='Is PLM')
    is_manufacture = fields.Boolean(string='IS Manufacture')
    # sale_line_id = fields.Many2one(required=True)
    # Is Manudature
    project_name_manufacture = fields.Char(string='Project Serial', readonly=True)
    project_type_manufacture = fields.Char(string='Project Name', readonly=True)
    project_type_name = fields.Char(string='Project Type', readonly=True)
    product_id_manufacture = fields.Integer(string='Product ID')
    assigned_to = fields.Many2one('hr.employee', string='Sales Person')
    company_name = fields.Many2one('res.company', string='Company Name')
    vendor_pill = fields.Many2one('account.move', string='Vendor Pill')
    pill_id = fields.Integer(string='Pill Id', relate='vendor_pill.id')

    product_save_id = fields.Integer(string='Save Product Id')

    # Method for create manufacturing order from smart button manufacturing order
    def get_manufacturing_order(self):

        for rec in self:
            get_id_product_save = rec.product_save_id
            get_id_product = rec.product_id_manufacture
            # Check if product_save_id has value and create manufacturing order
        if get_id_product_save == 0:
            get_mrp_id = self.env['mrp.production'].create({'product_id': get_id_product})
            rec.product_save_id = get_mrp_id.id

        for rec in self:
            get_stage_id = rec.stage_id
            get_id_product_save = rec.product_save_id

        if get_stage_id.name == 'New':
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'view_type': 'form',
                'view_mode': 'form',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'res_id': get_id_product_save,
                'view_type': 'form',
                'view_mode': 'form',
            }

    # Method to get purchasing order
    @api.onchange('vendor_pill')
    def get_purchasing_order(self):

        for rec in self:
            get_pill_id = rec.vendor_pill.id
            rec.pill_id = get_pill_id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': get_pill_id,
            'view_type': 'form',
            'view_mode': 'form',
        }
