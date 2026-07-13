from odoo import fields, models


class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'

    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.char('Description', required=False, translate=True)
    price = fields.Integer('price', required=True)
    


