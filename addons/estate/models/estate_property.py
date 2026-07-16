from odoo import fields, models
from datetime import timedelta, date


class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'

    def validade_padrao(self):
        return date.today() + timedelta(days=90)
    
    nome = fields.Char(string='Nome', required=True, translate=True)
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

