from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.produto.service import (
    criar_produto,
    editar_produto,
    excluir_produto,
    buscar_produto
)

produto_bp = Blueprint("produto", __name__)


@produto_bp.route("/cadastrar_produto", methods=["GET", "POST"])
@login_required
def cadastrar_produto():

    if current_user.perfil != "Administrador":
        flash(
            "Somente administradores podem cadastrar produtos.",
            "danger"
        )

        return redirect(url_for("estoque.ver_estoque"))

    if request.method == "POST":

        criar_produto(
            nome=request.form["nome"],

            valor=round(
                float(request.form["valor"]),
                2
            ),

            quantidade=int(
                request.form["quantidade"]
            ),

            quantidade_minima=int(
                request.form["quantidade_minima"]
            ),

            descricao=request.form["descricao"],

            usuario_id=current_user.id

        )

        flash(
            "Produto cadastrado com sucesso!",
            "success"
        )

        return redirect(
            url_for("estoque.ver_estoque")
        )

    return render_template(
        "cadastrar_produto.html"
    )


@produto_bp.route("/editar_produto/<int:id>", methods=["GET", "POST"])
@login_required
def editar_produto_route(id):
    if current_user.perfil != "Administrador":
        flash(
            "Somente administradores podem editar produtos.",
            "danger"
        )

        return redirect(url_for("estoque.ver_estoque"))

    produto = buscar_produto(id)

    if not produto:
        flash(
            "Produto não encontrado.",
            "danger"
        )

        return redirect(url_for("estoque.ver_estoque"))

    origem = request.args.get("origem", "estoque")

    if request.method == "POST":

        sucesso, mensagem = editar_produto(
            produto_id=id,
            nome=request.form["nomeForm"],
            descricao=request.form["descricaoForm"],
            valor=float(request.form["valorForm"]),
            quantidade_minima=int(request.form["quantidade_minimaForm"])
        )

        flash(mensagem, "success" if sucesso else "danger")

        if origem == "baixo_estoque":
            return redirect(url_for("estoque.produtos_baixo_estoque"))

        return redirect(url_for("estoque.ver_estoque"))

    return render_template(
        "editar_produto.html",
        produto=produto,
        origem=origem
    )


@produto_bp.route("/excluir_produto/<int:id>")
@login_required
def excluir_produto_route(id):
    if current_user.perfil != "Administrador":
        flash(
            "Somente administradores podem excluir produtos.",
            "danger"
        )

        return redirect(url_for("estoque.ver_estoque"))

    sucesso, mensagem = excluir_produto(id)

    flash(
        mensagem,
        "success" if sucesso else "danger"
    )

    return redirect(url_for("estoque.ver_estoque"))
