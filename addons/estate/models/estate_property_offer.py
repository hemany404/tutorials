from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "test_model_offer"
    _description = "Oferta de Propriedade"

    price = fields.Float(string="Preço")
    status = fields.Selection(
        selection=[
            ('accepted', 'Aceito'),
            ('refused', 'Recusado'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Parceiro", required=True)
    property_id = fields.Many2one("test_model", string="Propriedade", required=True)