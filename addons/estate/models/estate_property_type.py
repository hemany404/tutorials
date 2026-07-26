from odoo import fields, models


class TestModelType(models.Model):

    _name  = 'test_model_type'
    _description = 'Tipo de Propriedades'
    _rec_name = 'nome' 

    nome = fields.Char(string='Nome', required=True)
    property_ids = fields.One2many('test_model', 'tipo_propiedade', string='Propriedades')