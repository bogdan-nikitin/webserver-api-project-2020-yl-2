"""Модуль содержит основные обработчики тех страниц, которые будут видеть
обычные пользователи."""

from flask import Blueprint, render_template, redirect
from flask_login import current_user
from app.forms import LoginForm


blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    # TODO Заглушка. Может только отображать форму входа.
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            return redirect('/')
        param = {
            'title': 'Войти в PyMessages',
            'form': form
        }
        return render_template('login.html', **param)
    return
