from getpass import getpass

from app import create_app
from app.extensions.db import db
from app.models.usuario import Usuario


app = create_app()


with app.app_context():

    nome = input("Nome do administrador: ").strip()
    email = input("Email do administrador: ").strip()

    senha = getpass("Senha do administrador: ")
    confirmacao = getpass("Confirme a senha: ")

    if not nome:
        print("O nome é obrigatório.")
        exit()

    if not email:
        print("O email é obrigatório.")
        exit()

    if not senha:
        print("A senha é obrigatória.")
        exit()

    if senha != confirmacao:
        print("As senhas não coincidem.")
        exit()

    usuario_existente = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario_existente:
        print("Já existe um usuário com esse email.")
        exit()

    usuario = Usuario(
        nome=nome,
        email=email,
        perfil="Administrador"
    )

    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    print("Administrador criado com sucesso!")
