from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

core_bp = Blueprint("core", __name__)


@core_bp.route('/')
@login_required
def home():

    if current_user.perfil not in ["Administrador", "Comum"]:
        flash(
            "Você não tem permissão para acessar esta página.",
            "danger"
        )
        return redirect(url_for("usuario.login"))

    return render_template(
        "home.html",
        is_admin=current_user.perfil == "Administrador"
    )
