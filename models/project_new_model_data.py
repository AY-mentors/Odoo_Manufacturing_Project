import ast

import datetime as datetime

from odoo import api, fields, models, _


# Make new project type table in the database and make relation with table project_process
class ProjectType(models.Model):
    _name = 'project.type'
    _description = 'Project Type'
    _rec_name = 'name_of_project'

    name_of_project = fields.Char(string='Name', required=True)
    project_process = fields.One2many('project.process', 'relation_id', string="Data")


# Make new project process table in the database and make relation with table project_type
class ProjectProcess(models.Model):
    _name = 'project.process'
    _description = 'Project Process'

    sequence = fields.Integer(string='Sequence', required=True)
    process = fields.Char(string='Process', required=True)
    task_validity_days = fields.Integer(string="Task Validity Days")
    assignee = fields.Many2one('hr.employee', string='Assignee')
    task_type = fields.Selection([('main', 'Main Task'), ('sub', 'Sub Task')], string='Task Type')
    # dependent_task = fields.Many2one('project.subtask.type', domain="[('task_type', '=', 'Sub Task')]")
    dependent_task = fields.Many2one('project.subtask.type', string='Dependent Task',
                                     domain="[('project_id', '=', get_id_select)]")
    # dependent_task = fields.Char(string='Dependent Task')
    is_sample_order = fields.Boolean(string='Is Sample Order')
    is_procurement = fields.Boolean(string='Is Procurement')
    is_plm = fields.Boolean(string='Is PLM')
    is_manufacture = fields.Boolean(string='IS Manufacture')

    # name = fields.Char(string='Name')
    # age = fields.Integer(string='Age')
    # gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    relation_id = fields.Many2one('project.type', string='Project1')
    relation_id2 = fields.Many2one('sale.order', string='Project12')
    get_id_select = fields.Integer(string='Get Id', related='relation_id.id')
    record_id_subtask_id_save = fields.Integer(string='Subtask Id')

    # Override on create method
    @api.model
    def create(self, vals_list):
        # initial var
        record_id_project_id = 0
        record_id_subtask_id = 0

        # get project type id for record
        record_id = self.env['project.type'].search([])
        for rec in record_id:
            record_id_project_id = rec.id

        # get project process id for record
        record_id = self.env['project.process'].search([])
        for rec in record_id:
            record_id_subtask_id = rec.id
            vals_list['record_id_subtask_id_save'] = rec.id

        # set project type id and project process id into new table project_subtask_id
        if vals_list['task_type'] == 'sub':
            subtask_name = vals_list['process']
            self.env['project.subtask.type'].create(
                {'project_id': record_id_project_id, 'subtask_id': vals_list['record_id_subtask_id_save'],
                 'subtask_name': subtask_name})
            _rec_name = 'subtask_name'
            return super(ProjectProcess, self).create(vals_list)
        else:
            return super(ProjectProcess, self).create(vals_list)

    # Method to update table project process
    def update_process(self):
        for rec in self:
            get_id = rec.record_id_subtask_id_save
            get_name = rec.process

            self.env['project.subtask.type'].search([('subtask_id', '=', get_id)]).write(
                {'subtask_name': get_name})

    # Override on write method
    @api.model
    def write(self, vals_list):
        super(ProjectProcess, self).write(vals_list)
        return self.update_process()

    # Override on delete method
    @api.model
    def unlink(self):
        # "your code"
        for rec in self:
            get_id = rec.record_id_subtask_id_save
        self.env['project.subtask.type'].search([('subtask_id', '=', get_id)]).unlink()
        return super(ProjectProcess, self).unlink()


# Create tabel project_subtask_type
class ProjectSubTask(models.Model):
    _name = 'project.subtask.type'
    _description = 'Project Sub Task'
    _rec_name = 'subtask_name'

    project_id = fields.Integer(string="Project Id")
    subtask_id = fields.Integer(string="Task Id")
    subtask_name = fields.Char(string='Process')
