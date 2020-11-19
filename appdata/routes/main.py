from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from appdata.extensions import db
from appdata.models import User, Customer
from appdata.forms import RegisterForm, LoginForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    r_form = RegisterForm()
    l_form = LoginForm()
    context = {
        'registerForm': r_form,
        'loginForm': l_form,
        'openWindow': 0
    }
    return render_template('index.html', **context)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #successfully validated
        customer = Customer(
            user = User(
                login = form.reg_login.data,
                unhashed_password = form.reg_password.data
            ), 
            email = form.email.data
        )
        db.session.add(customer)
        db.session.commit()
        login_user(customer.user)
        return redirect(url_for('main.index'))
    else:
        # validation failed or GET
        context = {
            'registerForm': form,
            'loginForm': LoginForm(),
            'openWindow': 1
        }
        return render_template('index.html', **context)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #successfully validate
        login_user(User.query.filter_by(login=form.login.data).first())
        return redirect(url_for("main.index"))
    else:
        # validation failed or GET
        context = {
            'registerForm': RegisterForm(),
            'loginForm': form,
            'openWindow': 1
        }
        return render_template('index.html', **context)


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

