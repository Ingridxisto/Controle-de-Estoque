from app.extensions.db import db
from app.models.produto import Produto
from app.models.estoque import MovimentacaoEstoque


def criar_produto(
        nome,
        valor,
        quantidade,
        quantidade_minima,
        descricao,
        usuario_id
):

    produto = Produto(
        nome=nome,
        valor=valor,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima,
        descricao=descricao
    )

    db.session.add(produto)
    db.session.flush()

    movimentacao = MovimentacaoEstoque(
        produto_id=produto.id,
        quantidade=quantidade,
        tipo="entrada",
        usuario_id=usuario_id
    )

    db.session.add(movimentacao)
    db.session.commit()

    return produto


def buscar_produto(produto_id):
    return db.session.get(Produto, produto_id)


def editar_produto(produto_id, nome, descricao, valor, quantidade_minima):
    produto = buscar_produto(produto_id)

    if not produto:
        return False, "Produto não encontrado."

    produto.nome = nome
    produto.descricao = descricao
    produto.valor = valor
    produto.quantidade_minima = quantidade_minima

    db.session.commit()

    return True, "Produto atualizado com sucesso."


def excluir_produto(produto_id):
    produto = buscar_produto(produto_id)

    if not produto:
        return False, "Produto não encontrado."

    movimentacoes = MovimentacaoEstoque.query.filter_by(
        produto_id=produto_id
    ).all()

    for movimentacao in movimentacoes:
        db.session.delete(movimentacao)

    db.session.delete(produto)
    db.session.commit()

    return True, "Produto excluído com sucesso."
