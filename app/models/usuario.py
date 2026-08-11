from app.extensions.db import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import UserMixin


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True

    )
    nome = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        unique=True
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    perfil = db.Column(
        db.String(20),
        nullable=False
    )

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(
            self.senha,
            senha
        )

    def validar_perfil(self):
        return self.perfil in [
            "Administrador",
            "Comum"
        ]
