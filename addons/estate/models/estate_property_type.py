from odoo import fields, models


class TestModelType(models.Model):

    _name  = 'test_model_type'
    _description = 'Tipo de Propriedades'

    nome = fields.Char(string='Nome', required=True)