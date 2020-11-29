from flask import Blueprint, flash, render_template, request, redirect, url_for, session, g
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from appdata.extensions import db
from appdata.models import User, Customer, Hotel, Reservation, Visit
from appdata.forms import RegisterForm, LoginForm, ReservationForm
import base64

main = Blueprint('main', __name__)


@main.context_processor
def inject_hotels():
    hotels = Hotel.query.all()
    print('fffffffff')
    if not current_user.is_authenticated:
        print('F')
        registerForm = RegisterForm()
        loginForm = LoginForm()
        return dict(
            hotels=hotels,
            registerForm=registerForm,
            loginForm=loginForm
        )
    else:
        return dict(
            hotels=hotels
        )


@main.route('/')
def index():
    return render_template('index.html')

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
        return redirect(url_for('main.profile'))
    elif request.method == 'POST':
        # validation failed or GET
        context = {
            'registerForm': form,
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
        print('heeeeeeee')
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        # validation failed
        context = {
            'loginForm': form,
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
    return render_template('aboutus.html')

#o nás-historie -template
@main.route('/historie', methods=['GET'])
def history():
    return render_template('history.html')

#o služby-ubytovani -template
@main.route('/ubytovani', methods=['GET'])
def ubytovani():
    return render_template('ubytovani.html')

#o služby-sport -template
@main.route('/sport', methods=['GET'])
def sport():
    return render_template('sport.html')

#o služby-personal -template
@main.route('/personal', methods=['GET'])
def personal():
    return render_template('personal.html')

@main.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

@main.route('/<id>', methods=['GET'])
def hotel_overview(id):
    hotel = Hotel.query.filter_by(id=id).first()
    return render_template('room-types.html', hotel=hotel)

@main.route('/<id>/reservation', methods=['GET', 'POST'])
def reservation(id):
    form = ReservationForm()
    form.hotel_id = id
    context = {
        'hotel': Hotel.query.filter_by(id=id).first(),
        'resForm': form
    }
    if request.method == 'POST' and form.validate_on_submit():
        #form validation succsess
        desired_rooms_number = int(form.one_rooms.data)
        print(desired_rooms_number)
        
        avaiable_rooms = form.avaiable_rooms
        print(avaiable_rooms)
        if current_user.is_authenticated:
            try:
                tmp = Visit(
                    customer_id = current_user.login,
                    date_from = form.date_from.data,
                    date_to = form.date_to.data,
                    price = 2,
                    visit_type='RES'
                )
                tmp.rooms = []
                tmp.rooms = avaiable_rooms[:desired_rooms_number]
                db.session.add(tmp)
                res = Reservation(
                    visit = tmp,
                )
                db.session.add(res)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('Nastala neočekávaná chyba. Zkuste akci opakovat.')
                return redirect(url_for('main.reservation', id=id))
            return redirect(url_for('main.index'))
        else:
            flash("Děkujeme za rezervaci. Další informace máte na zadaném emailu.")
            return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #form validation failed
        context['resForm'] = form
    else:
        #get request
        context['resForm'] = form
    return render_template('reservation.html', **context)