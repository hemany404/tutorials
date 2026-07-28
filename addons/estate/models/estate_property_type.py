from odoo import fields, models, api


class TestModelType(models.Model):

    _name  = 'test_model_type'
    _description = 'Tipo de Propriedades'
    _rec_name = 'nome' 
    _order = "nome"

    nome = fields.Char(string='Nome', required=True)
    property_ids = fields.One2many('test_model', 'tipo_propiedade', string='Propriedades')
    offer_ids = fields.One2many('test_model_offer','property_type_id', string='Ofertas')

    offer_count = fields.Integer(compute="_compute_offer_count", string='Ofertas')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)