import os
import json

from flask import Blueprint
from flask import redirect, url_for, render_template, flash, jsonify
from flask import current_app, session
from flask_login import login_user, logout_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from ..models import db, User
from ..extensions import admin_permission
from ..forms import LoginForm, RegisterForm


bp_main = Blueprint(
    'main',
    __name__,
    static_folder='static',
    static_url_path='/main/static',
    template_folder='templates/main'
)


@bp_main.route('/')
def index():
    return redirect(url_for('blog.home'))


@bp_main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        kwargs = {}
        if 'ldf' in session:
            next_view = session['ldf']['name']
            kwargs = session['ldf']['kwargs']
            session.pop('ldf', None)
        else:
            next_view = 'home'

        flash('You have been logged in.', category='success')
        return redirect(url_for('blog.' + next_view, **kwargs))

    return render_template('login.html', form=form)


@bp_main.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_active:
        logout_user()

        identity_changed.send(
            current_app._get_current_object(),
            identity=AnonymousIdentity()
        )

        flash('You have been logged out.', category='success')

    return redirect(url_for('blog.home'))


@bp_main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        # new_user.roles = ['']
        db.session.add(new_user)
        db.session.commit()

        flash(
            'Your user has been created, please log in.',
            category='success'
        )

        return redirect(url_for('.login'))
    else:
        return render_template('register.html', form=form)


@bp_main.route('/current_user', methods=['GET'])
@admin_permission.require(http_exception=403)
def who_is_current_user():
    cu_dict = {}
    for item in dir(current_user):
        cu_dict[str(item)] = str(getattr(current_user, str(item)))
    return jsonify(cu_dict)


@bp_main.route('/flask_session', methods=['GET'])
@admin_permission.require(http_exception=403)
def flask_session_info():
    fs_dict = {}
    for item in dir(session):
        fs_dict[str(item)] = str(getattr(session, str(item)))
    return jsonify(fs_dict)
