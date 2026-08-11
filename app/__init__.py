from flask import Flask

from app.config import Config

from app.extensions.db import db
from app.extensions.migrate import migrate
from app.extensions.login import login_manager
from app.extensions.jwt import jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Models
    from app.models.usuario import Usuario
    from app.models.produto import Produto
    from app.models.estoque import MovimentacaoEstoque

    # Blueprints
    from app.core.routes import core_bp
    from app.usuario.routes import usuario_bp
    from app.produto.routes import produto_bp
    from app.estoque.routes import estoque_bp
    from app.api.routes import api_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(api_bp)

    return app
