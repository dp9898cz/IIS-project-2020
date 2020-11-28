from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from appdata.extensions import db
from appdata.models import User, Customer, Hotel
from appdata.forms import RegisterForm, LoginForm, ReservationForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    context = {
        'registerForm': RegisterForm(),
        'loginForm': LoginForm(),
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
    elif request.method == 'POST':
        # validation failed or GET
        context = {
            'registerForm': form,
            'loginForm': LoginForm(),
            'openWindow': 1
        }
        return render_template('index.html', **context)
    else:
        # GET method
        return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #successfully validate
        login_user(User.query.filter_by(login=form.login.data).first())
        return redirect(url_for("main.index"))
    elif request.method == 'POST':
        # validation failed
        context = {
            'loginForm': form,
            'registerForm' : RegisterForm(),
            'openWindow': 1
        }        
        return render_template('index.html', **context)
    else:
        # GET method
        return redirect(url_for('main.index'))


@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


#o nás-rentel -template
@main.route('/onas', methods=['GET'])
def onas():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('aboutus.html', **context)

#o nás-historie -template
@main.route('/historie', methods=['GET'])
def history():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('history.html', **context)

#hotely -hotel -template
@main.route('/hotel', methods=['GET'])
def hotel():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('hotel.html', **context)

#o služby -template
@main.route('/služby', methods=['GET'])
def services():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('services.html', **context)
#o služby-ubytovani -template
@main.route('/ubytovani', methods=['GET'])
def ubytovani():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('ubytovani.html', **context)

#o služby-sport -template
@main.route('/sport', methods=['GET'])
def sport():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 0
            }
    return render_template('sport.html', **context)

#o služby-personal -template
@main.route('/personal', methods=['GET'])
def personal():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 0
            }
    return render_template('personal.html', **context)

@main.route('/<id>', methods=['GET'])
def hotel_overview(id):
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 0,
                'hotel': Hotel.query.filter_by(id=id).first()
            }
    return render_template('room-types.html', **context)

@main.route('/<id>/reservation', methods=['GET', 'POST'])
def reservation(id):
    form = ReservationForm()
    form.hotel_id = id
    context = {
        'hotel': Hotel.query.filter_by(id=id).first()
    }
    if request.method == 'POST' and form.validate_on_submit():
        #form validation succsess
        print(request.form)
    elif request.method == 'POST':
        #form validation failed
        context['resForm'] = form
    else:
        #get request
        context['resForm'] = ReservationForm()

    if current_user == None or current_user.id == None:
        context['registerForm'] = RegisterForm()
        context['loginForm'] = LoginForm()
    return render_template('reservation.html', **context)