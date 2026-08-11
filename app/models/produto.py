from app.extensions.db import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    valor = db.Column(db.Float, nullable=False)

    quantidade = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    quantidade_minima = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    descricao = db.Column(db.String(255))
