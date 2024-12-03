from db import db


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_minima = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    movimentacoes = db.relationship(
        'MovimentacaoEstoque',
        cascade='all, delete-orphan',
        backref='produto_relacionado'
    )

    def __init__(self, nome, valor, quantidade, quantidade_minima, descricao):
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade
        self.quantidade_minima = quantidade_minima
        self.descricao = descricao
