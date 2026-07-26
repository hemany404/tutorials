from odoo import fields, models


class TestModelTag(models.Model):

    _name = 'test_model_tag'
    _description= 'Tags'
    _rec_name = 'nome' 

    nome = fields.Char(string='Nome', required=True)
    
    _sql_constraints = [
        ('unique_tag_name', 
         'UNIQUE(nome)', 
         'Já existe uma tag com este nome. Os nomes das tags devem ser únicos.'),
    ]

