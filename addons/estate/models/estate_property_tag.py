from odoo import fields, models


class TestModelTag(models.Model):

    _name = 'test_model_tag'
    _description= 'Tags'

    nome = fields.Char(string='Nome', required=True)