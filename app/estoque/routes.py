from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from app.estoque.service import (
    listar_produtos,
    produtos_baixo_estoque,
    movimentar_produto
)


estoque_bp = Blueprint(
    "estoque",
    __name__
)


@estoque_bp.route("/estoque")
@login_required
def ver_estoque():

    produtos = listar_produtos()

    return render_template(
        "ver_estoque.html",
        produtos=produtos,
        is_admin=current_user.perfil == "Administrador"
    )


@estoque_bp.route("/produtos_baixo_estoque")
@login_required
def listar_baixo_estoque():

    produtos = produtos_baixo_estoque()

    return render_template(
        "produtos_baixo_estoque.html",
        produtos=produtos
    )


@estoque_bp.route(
    "/movimentacao/<tipo>/<int:produto_id>",
    methods=["POST"]
)
@login_required
def movimentar(tipo, produto_id):

    if current_user.perfil != "Administrador":
        flash(
            "Somente administradores podem movimentar estoque.",
            "danger"
        )

        return redirect(
            url_for("estoque.ver_estoque")
        )

    # =========================
    # VALIDAÇÃO DA QUANTIDADE
    # =========================

    try:
        quantidade = int(request.form["quantidade"])

    except (KeyError, ValueError):
        flash(
            "Informe uma quantidade válida.",
            "danger"
        )

        return redirect(
            url_for("estoque.ver_estoque")
        )

    if quantidade <= 0:
        flash(
            "A quantidade deve ser maior que zero.",
            "danger"
        )

        return redirect(
            url_for("estoque.ver_estoque")
        )

    # =========================
    # VALIDAÇÃO DO TIPO
    # =========================

    if tipo not in ("entrada", "saida"):
        flash(
            "Tipo de movimentação inválido.",
            "danger"
        )

        return redirect(
            url_for("estoque.ver_estoque")
        )

    # =========================
    # MOVIMENTAÇÃO
    # =========================

    sucesso, mensagem = movimentar_produto(
        produto_id=produto_id,
        quantidade=quantidade,
        tipo=tipo,
        usuario_id=current_user.id
    )

    flash(
        mensagem,
        "success" if sucesso else "danger"
    )

    return redirect(
        url_for("estoque.ver_estoque")
    )
