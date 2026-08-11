from flask_login import LoginManager

from app.extensions.db import db
from app.models.usuario import Usuario

login_manager = LoginManager()

login_manager.login_view = 'usuario.login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))
