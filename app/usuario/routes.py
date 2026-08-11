from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from app.models.usuario import Usuario
from app.usuario.service import autenticar_usuario, criar_usuario

usuario_bp = Blueprint(
    "usuario",
    __name__
)


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form["nomeForm"]
        senha = request.form["senhaForm"]
        perfil = request.form["perfil"]

        usuario = autenticar_usuario(nome, senha)

        if usuario:
            if usuario.perfil != perfil:
                flash(
                    f'Perfil incorreto! Você está registrado como "{usuario.perfil}".',
                    "danger"
                )

                return redirect(url_for('usuario.login'))

            login_user(usuario)

            return redirect(url_for("core.home"))

        flash("Nome ou senha incorretos!", "danger")

    return render_template("login.html")


@usuario_bp.route('/logout')
def logout():

    logout_user()

    session.clear()

    flash("Você saiu da sua conta.", "info")

    return redirect(url_for("usuario.login"))


@usuario_bp.route("/cadastrar_usuario", methods=["GET", "POST"])
@login_required
def cadastrar_usuario():

    if current_user.perfil != "Administrador":

        flash(
            "Apenas administradores podem cadastrar novos usuários.",
            "danger"
        )

        return redirect(url_for("estoque.ver_estoque"))

    if request.method == "POST":

        sucesso, mensagem = criar_usuario(

            nome=request.form["nomeForm"],
            email=request.form["emailForm"],
            senha=request.form["senhaForm"],
            perfil=request.form["perfil"]

        )

        flash(
            mensagem,
            "success" if sucesso else "danger"
        )

        if sucesso:
            return redirect(
                url_for("usuario.cadastrar_usuario")
            )

    return render_template(
        "cadastrar_usuario.html"
    )
