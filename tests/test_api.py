import pytest

from app import create_app
from app.extensions.db import db
from app.models.usuario import Usuario
from app.models.produto import Produto


@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        usuario = Usuario(
            nome="admin_teste",
            email="admin@teste.com",
            perfil="Administrador"
        )
        usuario.set_senha("123456")

        usuario_comum = Usuario(
            nome="usuario_teste",
            email="usuario@teste.com",
            perfil="Comum"
        )
        usuario_comum.set_senha("123456")

        db.session.add_all([usuario, usuario_comum])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_api(client):

    resposta = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert "access_token" in dados
    assert dados["usuario"]["email"] == "admin@teste.com"
    assert dados["usuario"]["perfil"] == "Administrador"


def test_listar_produtos_com_token(client, app):

    with app.app_context():

        produto = Produto(
            nome="Notebook Teste",
            descricao="Produto para teste automatizado",
            valor=2500.00,
            quantidade=10,
            quantidade_minima=2
        )

        db.session.add(produto)
        db.session.commit()

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    assert token

    resposta = client.get(
        "/api/produtos",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert len(dados) == 1
    assert dados[0]["nome"] == "Notebook Teste"
    assert dados[0]["quantidade"] == 10


def test_listar_produtos_sem_token(client):

    resposta = client.get("/api/produtos")

    assert resposta.status_code == 401


def test_criar_produto_usuario_comum(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "usuario@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/produtos",
        json={
            "nome": "Produto Teste",
            "descricao": "Produto criado em teste",
            "valor": 100.00,
            "quantidade": 10,
            "quantidade_minima": 2
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 403


def test_criar_produto_administrador(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/produtos",
        json={
            "nome": "Mouse Gamer",
            "descricao": "Mouse para teste automatizado",
            "valor": 150.00,
            "quantidade": 20,
            "quantidade_minima": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["nome"] == "Mouse Gamer"
    assert dados["descricao"] == "Mouse para teste automatizado"
    assert dados["valor"] == 150.00
    assert dados["quantidade"] == 20
    assert dados["quantidade_minima"] == 5


def test_atualizar_produto_administrador(client, app):

    with app.app_context():

        produto = Produto(
            nome="Produto Original",
            descricao="Descricao Original",
            valor=100.00,
            quantidade=10,
            quantidade_minima=2
        )

        db.session.add(produto)
        db.session.commit()

        produto_id = produto.id

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.put(
        f"/api/produtos/{produto_id}",
        json={
            "nome": "Produto Atualizado",
            "descricao": "Descricao Atualizada",
            "valor": 250.00,
            "quantidade": 15,
            "quantidade_minima": 3
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["id"] == produto_id
    assert dados["nome"] == "Produto Atualizado"
    assert dados["descricao"] == "Descricao Atualizada"
    assert dados["valor"] == 250.00
    assert dados["quantidade"] == 15
    assert dados["quantidade_minima"] == 3


def test_excluir_produto_administrador(client, app):

    with app.app_context():

        produto = Produto(
            nome="Produto para Excluir",
            descricao="Produto usado no teste de DELETE",
            valor=50.00,
            quantidade=5,
            quantidade_minima=1
        )

        db.session.add(produto)
        db.session.commit()

        produto_id = produto.id

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.delete(
        f"/api/produtos/{produto_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["mensagem"] == "Produto excluído com sucesso"
    assert dados["id"] == produto_id


def test_criar_movimentacao_entrada(client, app):

    with app.app_context():

        produto = Produto(
            nome="Produto Estoque",
            descricao="Produto para teste de movimentação",
            valor=100.00,
            quantidade=10,
            quantidade_minima=2
        )

        db.session.add(produto)
        db.session.commit()

        produto_id = produto.id

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": produto_id,
            "tipo": "entrada",
            "quantidade": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["mensagem"] == "Movimentação registrada com sucesso"
    assert dados["movimentacao"]["produto_id"] == produto_id
    assert dados["movimentacao"]["tipo"] == "entrada"
    assert dados["movimentacao"]["quantidade"] == 5
    assert dados["movimentacao"]["estoque_atual"] == 15


def test_criar_movimentacao_saida(client, app):

    with app.app_context():

        produto = Produto(
            nome="Produto Saída",
            descricao="Produto para teste de saída",
            valor=100.00,
            quantidade=20,
            quantidade_minima=2
        )

        db.session.add(produto)
        db.session.commit()

        produto_id = produto.id

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": produto_id,
            "tipo": "saída",
            "quantidade": 8
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["mensagem"] == "Movimentação registrada com sucesso"
    assert dados["movimentacao"]["produto_id"] == produto_id
    assert dados["movimentacao"]["tipo"] == "Saída"
    assert dados["movimentacao"]["quantidade"] == 8
    assert dados["movimentacao"]["estoque_atual"] == 12


def test_saida_estoque_insuficiente(client, app):

    with app.app_context():

        produto = Produto(
            nome="Produto Teste",
            descricao="Teste estoque insuficiente",
            valor=100.00,
            quantidade=20,
            quantidade_minima=2
        )

        db.session.add(produto)
        db.session.commit()

        produto_id = produto.id

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": produto_id,
            "tipo": "saída",
            "quantidade": 100
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 400

    dados = resposta.get_json()

    assert dados["erro"] == "Estoque insuficiente."


def test_movimentacao_produto_inexistente(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": 9999,
            "tipo": "entrada",
            "quantidade": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 404

    dados = resposta.get_json()

    assert dados["erro"] == "Produto não encontrado"


def test_movimentacao_quantidade_zero(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": 1,
            "tipo": "entrada",
            "quantidade": 0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 400

    dados = resposta.get_json()

    assert dados["erro"] == "A quantidade deve ser maior que zero"


def test_movimentacao_quantidade_negativa(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": 1,
            "tipo": "entrada",
            "quantidade": -5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 400

    dados = resposta.get_json()

    assert dados["erro"] == "A quantidade deve ser maior que zero"


def test_movimentacao_tipo_invalido(client):

    resposta_login = client.post(
        "/api/login",
        json={
            "email": "admin@teste.com",
            "senha": "123456"
        }
    )

    assert resposta_login.status_code == 200

    token = resposta_login.get_json()["access_token"]

    resposta = client.post(
        "/api/movimentacoes",
        json={
            "produto_id": 1,
            "tipo": "Transferência",
            "quantidade": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 400

    dados = resposta.get_json()

    assert dados["erro"] == "O tipo deve ser entrada ou saída"
