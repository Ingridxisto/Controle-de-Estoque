from flask import Blueprint, jsonify, request

from app.models.usuario import Usuario
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)

from app.extensions.db import db
from app.models.produto import Produto
from app.models.estoque import MovimentacaoEstoque

from app.services.produto_service import ProdutoService
from app.services.estoque_service import EstoqueService

from app.utils.auth import administrador_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/login", methods=["POST"])
def login_api():

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "O corpo da requisição deve conter um JSON"
        }), 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios"
        }), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({
            "erro": "Email ou senha incorretos"
        }), 401

    if not usuario.verificar_senha(senha):
        return jsonify({
            "erro": "Email ou senha incorretos"
        }), 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "perfil": usuario.perfil
        }
    )

    return jsonify({
        "access_token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }
    }), 200


@api_bp.route("/produtos", methods=["GET"])
@jwt_required()
def listar_produtos():

    produtos = Produto.query.all()

    return jsonify([
        {
            "id": produto.id,
            "nome": produto.nome,
            "descricao": produto.descricao,
            "valor": produto.valor,
            "quantidade": produto.quantidade,
            "quantidade_minima": produto.quantidade_minima
        }
        for produto in produtos
    ])


@api_bp.route("/produtos", methods=["POST"])
@administrador_required
def criar_produto():

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "O corpo da requisição deve conter um JSON"
        }), 400

    campos_obrigatorios = [
        "nome",
        "descricao",
        "valor",
        "quantidade",
        "quantidade_minima"
    ]

    campos_ausentes = [
        campo
        for campo in campos_obrigatorios
        if campo not in data
    ]

    if campos_ausentes:
        return jsonify({
            "erro": "Campos obrigatórios ausentes",
            "campos": campos_ausentes
        }), 400

    try:
        valor = float(data["valor"])
        quantidade = int(data["quantidade"])
        quantidade_minima = int(data["quantidade_minima"])
    except ValueError:
        return jsonify({
            "erro": "Valor, quantidade e quantidade_minima devem ser números"
        }), 400

    if not data["nome"].strip():
        return jsonify({
            "erro": "O nome do produto não pode ser vazio"
        }), 400

    if valor < 0:
        return jsonify({
            "erro": "O valor não pode ser negativo"
        }), 400

    if quantidade < 0:
        return jsonify({
            "erro": "A quantidade não pode ser negativa"
        }), 400

    if quantidade_minima < 0:
        return jsonify({
            "erro": "A quantidade mínima não pode ser negativa"
        }), 400

    produto = ProdutoService.criar_produto(
        nome=data["nome"].strip(),
        descricao=data["descricao"].strip(),
        valor=valor,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima
    )

    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "valor": produto.valor,
        "quantidade": produto.quantidade,
        "quantidade_minima": produto.quantidade_minima
    }), 201


@api_bp.route("/produtos/<int:produto_id>", methods=["GET"])
@jwt_required()
def buscar_produto(produto_id):

    produto = db.session.get(Produto, produto_id)

    if not produto:
        return jsonify({
            "error": "Produto nao encontrado"
        }), 404

    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "valor": produto.valor,
        "quantidade": produto.quantidade,
        "quantidade_minima": produto.quantidade_minima
    })


@api_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
@administrador_required
def atualizar_produto(produto_id):

    produto = db.session.get(Produto, produto_id)

    if produto is None:
        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "O corpo da requisição deve conter um JSON"
        }), 400

    campos_obrigatorios = [
        "nome",
        "descricao",
        "valor",
        "quantidade",
        "quantidade_minima"
    ]

    campos_ausentes = [
        campo
        for campo in campos_obrigatorios
        if campo not in data
    ]

    if campos_ausentes:
        return jsonify({
            "erro": "Campos obrigatórios ausentes",
            "campos": campos_ausentes
        }), 400

    try:
        valor = float(data["valor"])
        quantidade = int(data["quantidade"])
        quantidade_minima = int(data["quantidade_minima"])
    except (ValueError, TypeError):
        return jsonify({
            "erro": "Valor, quantidade e quantidade_minima devem ser números"
        }), 400

    nome = data["nome"].strip()
    descricao = data["descricao"].strip()

    if not nome:
        return jsonify({
            "erro": "O nome do produto não pode ser vazio"
        }), 400

    if valor < 0:
        return jsonify({
            "erro": "O valor não pode ser negativo"
        }), 400

    if quantidade < 0:
        return jsonify({
            "erro": "A quantidade não pode ser negativa"
        }), 400

    if quantidade_minima < 0:
        return jsonify({
            "erro": "A quantidade mínima não pode ser negativa"
        }), 400

    produto = ProdutoService.atualizar_produto(
        produto=produto,
        nome=nome,
        descricao=descricao,
        valor=valor,
        quantidade=quantidade,
        quantidade_minima=quantidade_minima
    )

    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "valor": produto.valor,
        "quantidade": produto.quantidade,
        "quantidade_minima": produto.quantidade_minima
    }), 200


@api_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
@administrador_required
def excluir_produto(produto_id):

    produto = db.session.get(Produto, produto_id)

    if not produto:
        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    movimentacoes = MovimentacaoEstoque.query.filter_by(
        produto_id=produto.id
    ).all()

    for movimentacao in movimentacoes:
        db.session.delete(movimentacao)

    ProdutoService.excluir_produto(produto)

    return jsonify({
        "mensagem": "Produto excluído com sucesso",
        "id": produto_id
    }), 200


@api_bp.route("/movimentacoes", methods=["POST"])
@administrador_required
def criar_movimentacao():

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "O corpo da requisição deve conter um JSON"
        }), 400

    produto_id = data.get("produto_id")
    tipo = data.get("tipo")
    quantidade = data.get("quantidade")

    if produto_id is None or tipo is None or quantidade is None:
        return jsonify({
            "erro": "produto_id, tipo e quantidade são obrigatórios"
        }), 400

    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)
    except (ValueError, TypeError):
        return jsonify({
            "erro": "produto_id e quantidade devem ser números"
        }), 400

    if produto_id <= 0:
        return jsonify({
            "erro": "O produto_id deve ser maior que zero"
        }), 400

    if quantidade <= 0:
        return jsonify({
            "erro": "A quantidade deve ser maior que zero"
        }), 400

    if tipo not in ["entrada", "saída"]:
        return jsonify({
            "erro": "O tipo deve ser 'entrada' ou 'saída'"
        }), 400

    produto = db.session.get(Produto, produto_id)

    if not produto:
        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    usuario_id = int(get_jwt_identity())

    try:

        movimentacao = EstoqueService.registrar_movimentacao(
            produto=produto,
            usuario_id=usuario_id,
            tipo=tipo,
            quantidade=quantidade
        )

    except ValueError as erro:

        return jsonify({
            "erro": str(erro)
        }), 400

    return jsonify({
        "mensagem": "Movimentação registrada com sucesso",
        "movimentacao": {
            "id": movimentacao.id,
            "produto_id": movimentacao.produto_id,
            "usuario_id": movimentacao.usuario_id,
            "tipo": movimentacao.tipo,
            "quantidade": movimentacao.quantidade,
            "estoque_atual": produto.quantidade,
            "data": movimentacao.data.isoformat()
        }
    }), 201


@api_bp.route("/movimentacoes", methods=["GET"])
@administrador_required
def listar_movimentacoes():

    movimentacoes = MovimentacaoEstoque.query.order_by(
        MovimentacaoEstoque.data.desc()
    ).all()

    return jsonify([
        {
            "id": movimentacao.id,

            "produto": {
                "id": movimentacao.produto_id,
                "nome": movimentacao.produto.nome
            },

            "usuario": {
                "id": movimentacao.usuario_id,
                "nome": movimentacao.usuario.nome
            },

            "tipo": movimentacao.tipo,
            "quantidade": movimentacao.quantidade,
            "data": movimentacao.data.isoformat()
        }
        for movimentacao in movimentacoes
    ]), 200
