from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo import _
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta, date


class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'
    _rec_name = 'nome' 
    _order = 'id desc'

    def validade_padrao(self):
        return date.today() + timedelta(days=90)

    nome = fields.Char(string='Nome', required=True, translate=True)
    tipo_propiedade = fields.Many2one('test_model_type',string='Tipo de propriedade')
    descricao = fields.Char(string='Descricao', required=False)
    codigo_postal = fields.Char(string='codigo_postal', required=False)
    data_disponivel = fields.Date(string='data_disponivel',copy=False, default=validade_padrao)
    preco_esperado = fields.Float(string='preco_esperado',required=True)
    preco_venda = fields.Float(string='Preco_venda',readonly=True, copy=False)
    quartos = fields.Integer(string="quartos", default=2,required=True)
    area_estar = fields.Integer(string='area_estar', required=True)
    fachadas = fields.Integer('fachadas')
    garagem = fields.Boolean('garagem')
    jardim = fields.Boolean('jardim')
    sequence = fields.Integer(default=10)
    @api.onchange('jardim')
    def _onchange_jardim(self):
        if self.jardim:
           self.jardim_area = 10
           self.jardim_orientacao = 'norte'

    jardim_area = fields.Integer('jardim_area')
    jardim_orientacao = fields.Selection(string='orientacao',
                                         selection=[('norte', 'norte'), ('sul', 'sul')],
                                         help='usado para escolher orientacao')
    state = fields.Selection(
    selection=[
        ('new', 'Novo'),
        ('offer_received', 'Oferta Recebida'),
        ('offer_accepted', 'Oferta Aceita'),
        ('sold', 'Vendido'),
        ('canceled', 'Cancelado')
    ],
    string="Status",
    required=True,
    copy=False,
    default='new')        
    active = fields.Boolean(string="Ativo", default=True)
    comprador_id = fields.Many2one('res.partner', string='comprador', copy=False)
    vendedor_id = fields.Many2one('res.users', string='vendedor',defualt=lambda self: self.env.user)
    tag_ids = fields.Many2many("test_model_tag", string="Tags")
    offer_ids = fields.One2many("test_model_offer", "property_id", string="Ofertas")
    best_price = fields.Float(compute='_compute_best_price', string='Melhor preco')
    total_area = fields.Float(compute='_compute_total_area', string='Area total')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
       lista = []
       for x in self.offer_ids:
          lista.append(x.price)
       if not lista:
          self.best_price = 0
       else:   
          self.best_price = max(lista)

    """def _compute_best_price(self):
    for property in self:
        if property.offer_ids:
            property.best_price = max(property.offer_ids.mapped('price'))
        else:
            property.best_price = 0.0"""     
     
    @api.depends('area_estar','jardim_area')
    def _compute_total_area(self):
      for property in self:
        property.total_area = (property.area_estar or 0.0) + (property.jardim_area or 0.0)


    def action_cancel(self):
        for record in self:
           
            if record.state == 'sold':
                raise UserError(_("Propriedades vendidas não podem ser canceladas."))
            
            record.state = 'canceled'
        
        return True
    
    def action_sold(self):
        for prop in self:
            if prop.state == 'canceled':
                raise UserError(_("Não é possível vender uma propriedade cancelada."))
            prop.state = 'sold'
        return True
    
    _sql_constraints = [
          ('unique_type_name', 
             'UNIQUE(nome)', 
             'Já existe um tipo de propriedade com este nome. Os nomes devem ser únicos.'),
        ]

    _sql_constraints = [
              ('check_expected_price_positive', 
         'CHECK(preco_esperado > 0)', 
         'O preço esperado deve ser estritamente positivo (maior que zero).'),

                ('check_selling_price_non_negative', 
         'CHECK(preco_venda >= 0)', 
         'O preço de venda não pode ser negativo.'),
    ]   

    @api.constrains('preco_venda', 'preco_esperado')
    def _check_selling_price_constraint(self):
        for record in self:
            # 1. Se o preço de venda for zero (ou próximo de zero), significa que a propriedade ainda não foi vendida.
            #    Nesse caso, a validação não se aplica (pula a verificação).
            if float_is_zero(record.preco_venda, precision_digits=2):
                continue

            # 2. Calcula o preço mínimo permitido (90% do esperado)
            min_allowed_price = record.preco_esperado * 0.9

            # 3. Compara o preço de venda com o mínimo permitido.
            #    float_compare(a, b, precision) retorna:
            #      -1 se a < b
            #       0 se a == b
            #       1 se a > b
            if float_compare(record.preco_venda, min_allowed_price, precision_digits=2) < 0:
                raise ValidationError(_(
                    "O preço de venda (%.2f) não pode ser inferior a 90%% do preço esperado (%.2f). "
                    "Preço mínimo permitido: %.2f"
                ) % (record.preco_venda, record.preco_esperado, min_allowed_price))

            def unlink(self):
                for record in self:
                    if record.state not in ['new','canceled']:
                        raise UserError(_(
                    "Não é possível excluir uma propriedade com status '%s'. "
                    "Apenas propriedades 'Novo' ou 'Cancelado' podem ser excluídas."
                ) % record.state)

                    