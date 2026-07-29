from odoo import fields, models, api, _
from datetime import date
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "test_model_offer"
    _description = "Oferta de Propriedade"
    _order = "price desc"
    _rec_name = "price"

    price = fields.Float(string="Preço")
    status = fields.Selection(
        selection=[
            ('accepted', 'Aceito'),
            ('refused', 'Recusado'),
        ],
        string="Status",
        copy=False,
    )
    validaty = fields.Integer(string='Validade', default=7)
    data_limite = fields.Date(compute='_compute_data_limite',inverse='_inverse_data_limite', string='Data Limite')
    property_type_id = fields.Many2one('test_model_type', 
                                    related='property_id.tipo_propiedade', 
                                    store=True,  
                                    string="Tipo de Propriedade")

    @api.depends('validaty')
    def _compute_data_limite(self):
        if self.create_date and self.validaty:
            self.data_limite = fields.Date.add(self.create_date, days=self.validaty)
        else:
            self.data_limite=False  

    def _inverse_data_limite(self):
            if self.data_limite and self.create_date:
                delta = (self.data_limite - self.create_date.date()).days
                self.validaty = max(delta, 1)  

    partner_id = fields.Many2one("res.partner", string="Parceiro", required=True)
    property_id = fields.Many2one("test_model", string="Propriedade", required=True)  # ligacao entre as tabelas

    def action_accept(self):
            # Garante que está agindo em apenas uma oferta (segurança)
            self.ensure_one()
            
            # Verifica se já existe uma oferta aceita para esta propriedade
            property_obj = self.property_id
            accepted_offers = property_obj.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError(_("Já existe uma oferta aceita para esta propriedade."))
            
            # Atualiza o status da oferta atual
            self.status = 'accepted'
            
            # Atualiza a propriedade com o preço e o comprador da oferta
            property_obj.preco_venda = self.price
            property_obj.comprador_id = self.partner_id
            property_obj.state = 'offer_accepted'

            
            # (Opcional) Recusa automaticamente as outras ofertas pendentes
            other_offers = property_obj.offer_ids.filtered(lambda o: o != self and o.status == 'new')
            other_offers.write({'status': 'refused'})
            
            return True

    def action_refuse(self):
            self.ensure_one()

            property_obj = self.property_id
            accepted_offers = property_obj.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError(_("Esta oferta já foi aceite."))
            self.status = 'refused'
            return True

    _sql_constraints = [

        ('check_offer_price_positive', 
         'CHECK(price > 0)', 
         'O preço da oferta deve ser estritamente positivo (maior que zero).'),
    ]


    @api.model
    def create(self, vals):

         values = vals[0]
         property_id = values.get('property_id')
         
         if property_id :
              property_obj = self.env['test_model'].browse(property_id)


              offer_price = values.get('price')
              if property_obj.offer_ids:
                   max_price = max(property_obj.offer_ids.mapped('price'))
                   if offer_price < max_price:
                        raise UserError(_(
                        "O preço da oferta (%.2f) não pode ser menor que a maior oferta existente (%.2f) "
                        "para esta propriedade." % (offer_price, max_price)
                    ))

              property_obj.state = 'offer_received'   

         return super().create(vals)       