from odoo import fields, models


class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'
    _order = "sequence"

    nome = fields.Char('Nome', required=True, translate=True)
    descricao = fields.Char('Descricao', required=False)
    codigo_postal = fields.Char('codigo_posta', required=False)
    data_disponivel = fields.Date('data_disponivel', required=False)
    preco_esperado = fields.Float('preco_esperado',required=True)
    preco_venda = fields.Float('Preco_venda', required=True)
    quartos = fields.Integer('quartos', required=True)
    area_estar = fields.Integer('area_estar', required=True)
    fachadas = fields.Integer('fachadas', required=True)
    garagem = fields.Boolean('garagem', required=False)
    jardim = fields.Boolean('jardim', required=False)
    jardim_area = fields.Integer('jardim_area', required=True)
    jardim_orientacao = fields.Selection(string='orientacao',
                                         selection=[('norte', 'norte'), ('sul', 'sul')],
                                         help='usado para escolher orientacao')


