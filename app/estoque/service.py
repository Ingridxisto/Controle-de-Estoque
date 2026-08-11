from app.extensions.db import db
from app.models.produto import Produto
from app.models.estoque import MovimentacaoEstoque


def listar_produtos():
    return Produto.query.all()


def produtos_baixo_estoque():
    return Produto.query.filter(
        Produto.quantidade <= Produto.quantidade_minima
    ).all()


def movimentar_produto(
    produto_id,
    quantidade,
    tipo,
    usuario_id
):

    produto = db.session.get(
        Produto,
        produto_id
    )

    if not produto:
        return False, "Produto não encontrado."

    if quantidade <= 0:
        return False, "A quantidade deve ser maior que zero."

    if tipo == "entrada":
        produto.quantidade += quantidade

    elif tipo == "saida":
        if produto.quantidade < quantidade:
            return False, "Estoque insuficiente."

        produto.quantidade -= quantidade

    else:
        return False, "Tipo de movimentação inválido."

    movimentacao = MovimentacaoEstoque(
        produto_id=produto.id,
        quantidade=quantidade,
        tipo=tipo,
        usuario_id=usuario_id
    )

    db.session.add(movimentacao)

    db.session.commit()

    return True, "Movimentação realizada com sucesso."
