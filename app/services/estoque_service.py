from app.extensions.db import db
from app.models.estoque import MovimentacaoEstoque


class EstoqueService:

    @staticmethod
    def registrar_movimentacao(
        produto,
        usuario_id,
        tipo,
        quantidade
    ):

        if quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        if tipo not in ["entrada", "saída"]:
            raise ValueError(
                "O tipo de movimentação deve ser 'entrada' ou 'saída'."
            )

        if tipo == "saída" and produto.quantidade < quantidade:
            raise ValueError(
                "Estoque insuficiente."
            )

        if tipo == "entrada":
            produto.quantidade += quantidade

        else:
            produto.quantidade -= quantidade

        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            usuario_id=usuario_id,
            tipo=tipo,
            quantidade=quantidade
        )

        db.session.add(movimentacao)
        db.session.commit()

        return movimentacao
