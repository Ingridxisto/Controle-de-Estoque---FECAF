from db import db
from datetime import datetime


class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    produto = db.relationship('Produto', back_populates='movimentacoes')
    usuario = db.relationship('Usuario', backref=db.backref('movimentacoes', lazy=True))

    def __init__(self, produto_id, quantidade, tipo, usuario_id):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.tipo = tipo
        self.usuario_id = usuario_id
