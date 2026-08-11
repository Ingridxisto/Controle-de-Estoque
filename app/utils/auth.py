from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    get_jwt,
    jwt_required
)


def administrador_required(func):

    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        perfil = claims.get("perfil")

        if perfil != "Administrador":
            return jsonify({
                "erro": "Acesso permitido apenas para administradores"
            }), 403

        return func(*args, **kwargs)

    return wrapper
