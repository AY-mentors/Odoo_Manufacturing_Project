import ast

import datetime as datetime
from odoo import api, fields, models, _


# Inherit sale_order model and make modify
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name_tree = fields.Many2one('project.type', string="Project Type")
    # product_name_tree = fields.Many2one('project.type', string="Project Type")
    # project_get_product_name = fields.Many2one('sale.order.line', string="Project Order Line")
    project_process_tree = fields.One2many('project.process', 'relation_id2', string='Data')
    tasks_count_field = fields.Integer(string='Tasks count', compute="tasks_count_compute")
    tasks_id_field = fields.Integer(string='task_id')

    project_title = fields.Char(string="Project Title", required=True)
    scope_of_work = fields.Text(string="Scope Of Work", required=True)

    current_date = datetime.datetime.now().date()
    start_date = fields.Date(string="Start Date", required=True, default=current_date)
    end_date = fields.Date(string="End Date", required=True, default=current_date)

    # Show date in tree view for relation one2many from table project_process
    @api.onchange('project_name_tree')
    def _onchange_data_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            # lines = []
            for line in self.project_name_tree.project_process:
                vals = {
                    # 'relation_id': line.id,
                    'sequence': line.sequence,
                    'process': line.process,
                    'task_validity_days': line.task_validity_days,
                    'assignee': line.assignee,
                    'task_type': line.task_type,
                    'dependent_task': line.dependent_task,
                    'is_sample_order': line.is_sample_order,
                    'is_procurement': line.is_procurement,
                    'is_plm': line.is_plm,
                    'is_manufacture': line.is_manufacture
                }
                lines.append((0, 0, vals))
            rec.project_process_tree = lines

    # Method to create stages into table project_task
    def create_stages_done(self):
        sale_project_name = 0
        sale_project_type = 0

        # get last id insert into table sale_order_line
        for rec in self:
            sale_project_name = rec.name
            project_type_name = rec.project_name_tree.name_of_project

        get_sale_project_type_1 = self.env['sale.order.line'].search([], order='id desc')[0].id
        get_sale_project_type = self.env['sale.order.line'].search([('id', '=', get_sale_project_type_1)])

        for rec in get_sale_project_type:
            sale_project_type = rec.name
            get_sale_product_id = rec.product_id
        # Check if those stages into table project_task_type
        if self.env['project.task.type'].search(
                ['|', '|', '|', '|', '|', '|', ('name', '=', 'New Step'), ('name', '=', 'In Progress Step'),
                 ('name', '=', 'Done Step'),
                 ('name', '=', 'Cancelled Step'), ('name', '=', 'To Approved Step'), ('name', '=', 'Approved Step'),
                 ('name', '=', 'Waiting Customer Feedback Step')]):
            ''
        else:
            stage_type = ['New Step', 'In Progress Step', 'Done Step', 'Cancelled Step', 'To Approved Step',
                          'Approved Step', 'Waiting Customer Feedback Step']
            for stage in stage_type:
                self.env['project.task.type'].create({
                    'name': stage
                })
        # Create new project name
        project_name = self.project_title
        data_id = self.env['project.project'].create({'name': project_name})
        # Add project name to stages
        self.env['project.task.type'].search(
            ['|', '|', '|', '|', '|', '|', ('name', '=', 'New Step'), ('name', '=', 'In Progress Step'),
             ('name', '=', 'Done Step'),
             ('name', '=', 'Cancelled Step'), ('name', '=', 'To Approved Step'), ('name', '=', 'Approved Step'),
             ('name', '=', 'Waiting Customer Feedback Step')]).write({
            'project_ids': [(4, data_id.id)]})

        # Send Id To Task Id
        self.tasks_id_field = data_id.id

        # Create new project task
        # task_name = ''
        for line in self.project_name_tree.project_process:
            task_name = line.process
            is_sample_order = line.is_sample_order
            is_procurement = line.is_procurement
            is_plm = line.is_plm
            is_manufacture = line.is_manufacture

            self.env['project.task'].create({
                # 'relation_id': line.id,
                'name': task_name,
                'project_name_manufacture': sale_project_name,
                'project_type_manufacture': sale_project_type,
                'product_id_manufacture': get_sale_product_id,
                'project_type_name': project_type_name,
                'project_id': data_id.id,
                'is_sample_order': is_sample_order,
                'is_procurement': is_procurement,
                'is_plm': is_plm,
                'is_manufacture': is_manufacture,
            })

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Everything is correctly Done...',
                'type': 'rainbow_man',
            }
        }

    # Method to get project_task count
    @api.onchange('tasks_id_field')
    def tasks_count_compute(self):
        for rec in self:
            tasks_count = self.env['project.task'].search_count([('project_id', '=', rec.tasks_id_field)])
            rec.tasks_count_field = tasks_count

    # Method to compute date
    @api.onchange('end_date')
    def tasks_date_get_compute(self):
        # current_date = datetime.datetime.now().date()
        # new_date = current_date + datetime.timedelta(days=10)
        for rec in self:
            ooo_date = rec.end_date + datetime.timedelta(days=-10)
            rec.start_date = ooo_date

    # Method to open tasks from smart button tasks
    def action_open_tasks(self):
        for rec in self:
            tasks_id = rec.tasks_id_field
            project_title = rec.project_title

        action = self.env['ir.actions.act_window'].with_context({'active_id': tasks_id})._for_xml_id(
            'project.act_project_project_2_project_task_all')
        action['display_name'] = _("%(name)s", name=project_title)
        context = action['context'].replace('active_id', str(tasks_id))
        context = ast.literal_eval(context)
        context.update({
            'active_id': tasks_id,
        })
        action['context'] = context
        return action

    # Override on action_confirm button
    def action_confirm(self):
        self.create_stages_done()
        res = super(SaleOrder, self).action_confirm()
        return res

    # with open('invoice_details.csv', 'w') as fp:
    #     writer = csv.writer(fp)
    #     writer.writerow(['One', 'Tow', 'Three'])
    #     writer.writerows(['1', '2', '3'])
    #
    # with open('export.csv', mode='w') as file:
    #
    #     writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     # create a row contains heading of each column
    #     writer.writerow(
    #         ['ProductName', 'UOM', 'Price', 'Amount'])
    #     # fetch products and write respective data.
    #     for product in self.env['product.product']:
    #         name = product.product_tmpl_id.name
    #         uom = product.product_tmpl_id.uom_id.name
    #         price = product.product_tmpl_id.list_price
    #         amount = product.product_tmpl_id.taxes_id.amount
    #         writer.writerow([name, uom, price, amount])
    #
    # with open('export.csv', 'r', encoding="utf-8") as f2:
    #     # file encode and store in a variable ‘data’
    #     data = str.encode(f2.read(), 'utf-8')
