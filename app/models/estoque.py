from app.extensions.db import db
from datetime import datetime


class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacoes_estoque"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    produto = db.relationship("Produto")
    usuario = db.relationship("Usuario")

    tipo = db.Column(
        db.String(10),
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
