from odoo import fields, models


class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'
    _order = "sequence"

    nome = fields.Char('Nome', required=True, translate=True)
    descricao = fields.char('Descricao', required=False)
    codigo_postal = fields.char('codigo_posta', required=False)
    data_disponivel = fields.date('data_disponivel', required=False)
    preco_esperado = fields.float('preco_esperado',required=True)
    preco_venda = fields.float('Preco_venda', required=True)
    quartos = fields.integer('quartos', required=True)
    area_estar = fields.integer('area_estar', required=True)
    fachadas = fields.integer('fachadas', required=True)
    garagem = fields.float('garagem', required=True)
    jardim = fields.float('jardim', required=False)
    jardim_area = fields.integer('jardim_area', required=True)
    jardim_orientacao = fields.char('jardim_orientacao',required=False)


