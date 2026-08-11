import re

from app.extensions.db import db
from app.models.usuario import Usuario


def senha_valida(senha):
    """
    A senha deve possuir pelo menos 6 caracteres."""

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9@#$%^&+=]{6,}", senha
        )
    )


def autenticar_usuario(nome, senha):
    """
    Busca o usuário pelo nome e verifica a senha.
    Retorna o usuário se estiver correto, caso contrário retorna None.
    """

    usuario = Usuario.query.filter_by(nome=nome).first()

    if usuario and usuario.verificar_senha(senha):
        return usuario

    return None


def criar_usuario(nome, email, senha, perfil):

    if not nome:
        return False, "Nome é obrigatório."

    if not email:
        return False, "Email é obrigatório."

    if "@" not in email:
        return False, "Informe um email válido."

    if not senha:
        return False, "Senha é obrigatória."

    if len(senha) < 6:
        return False, "Senha deve ter no mínimo 6 caracteres."

    if not senha_valida(senha):
        return len(senha) >= 6, "Senha deve conter apenas letras, números e caracteres especiais @#$%^&+="

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        return False, "Este email já está cadastrado."

    if perfil not in ["Administrador", "Comum"]:
        return False, "Perfil inválido."

    usuario = Usuario(
        nome=nome,
        email=email,
        perfil=perfil
    )

    if not usuario.validar_perfil():
        return False, "Perfil inválido."

    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return True, "Usuário cadastrado com sucesso!"
