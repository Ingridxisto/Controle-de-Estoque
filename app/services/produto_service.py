from app.extensions.db import db
from app.models.produto import Produto


class ProdutoService:

    @staticmethod
    def criar_produto(
        nome,
        descricao,
        valor,
        quantidade,
        quantidade_minima
    ):
        produto = Produto(
            nome=nome,
            descricao=descricao,
            valor=valor,
            quantidade=quantidade,
            quantidade_minima=quantidade_minima
        )

        db.session.add(produto)
        db.session.commit()

        return produto

    @staticmethod
    def atualizar_produto(
        produto,
        nome,
        descricao,
        valor,
        quantidade,
        quantidade_minima
    ):
        produto.nome = nome
        produto.descricao = descricao
        produto.valor = valor
        produto.quantidade = quantidade
        produto.quantidade_minima = quantidade_minima

        db.session.commit()

        return produto

    @staticmethod
    def excluir_produto(produto):

        db.session.delete(produto)
        db.session.commit()

        return produto
