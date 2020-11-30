from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from appdata.models import User, Employee, Customer, Hotel, Room, Past, Visit, Ongoing, room_visit, Reservation
from appdata.extensions import csrf, db

dash = Blueprint('dash', __name__)
csrf.exempt(dash)


"""
User view CRUD
    only admin rights

"""
@dash.route('/dashboard')
@login_required
def dash_index():
    if not current_user.isEmployee:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_index.html')

@dash.route('/dashboard/users', methods=['GET', 'POST'])
@login_required
def user_index():
    if not current_user.employees.isAdmin:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #handle search request -> set cookie and redirect to the main user page
        login_filter = request.form['user_filter']
        if (login_filter):
            users = User.query.filter(User.login.contains(login_filter)).all()
        else:
            users = User.query.order_by(User.isEmployee.desc()).all()
        hotels = Hotel.query.all()
        resp = make_response(render_template('dashboard_users.html', filter=login_filter, hotels=hotels, users=users))
        resp.set_cookie('filter', login_filter)
        resp.headers['location'] = url_for('dash.user_index') 
        return resp, 302
    else:
        # main user page (apply search results filter if any)
        user_filter = request.cookies.get('filter')
        if (user_filter):
            users = User.query.filter(User.login.contains(user_filter)).all()
        else:
            users = User.query.order_by(User.isEmployee.desc()).all()
        hotels = Hotel.query.all()
        return render_template('dashboard_users.html', filter=user_filter, hotels=hotels, users=users)

@dash.route('/dashboard/users/update', methods=['POST'])
@login_required
def update_user():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        old_user_obj = User.query.filter_by(id = request.form['old_id']).first()
        if (old_user_obj.login != request.form['login']):
            #changing the login -> have to check if its free
            temp = User.query.filter_by(login=request.form['login']).first()
            if temp != None:
                flash('Tento login už existuje. Použijte jiný.')
                return redirect(url_for('dash.user_index'))
        try:
            # change all fields
            if (request.form.get('password') != ''):
                old_user_obj.unhashed_password = request.form.get('password')
            if old_user_obj.isEmployee:
                if (old_user_obj.employees.isAdmin and old_user_obj.id == current_user.id):
                    # admin cant change admin right to itself
                    flash("We dont do that here.")
                    return redirect(url_for('dash.user_index'))
                else:
                    employee = old_user_obj.employees
                    employee.isAdmin = 'on' == request.form.get('isAdmin')
                    employee.isOwner = 'on' == request.form.get('isOwner')
                    employee.isManager = 'on' == request.form.get('isManager')
                    employee.email = request.form.get('email')
                    employee.hotel_id = request.form.get('hotel')
            else:
                customer = old_user_obj.customers
                customer.email = request.form.get('email') if request.form.get('email') != '' else None
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Nastala chyba při aktualizaci údajů. Zkontrolujte údaje a opakujte akci.' + str(e))
        return redirect(url_for('dash.user_index'))

@dash.route('/dashboard/users/delete', methods=['POST'])
@login_required
def user_delete():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            usr = User.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(usr)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.user_index'))


@dash.route('/dashboard/users/create', methods=['POST'])
@login_required
def user_create():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            if 'on' == request.form.get('isEmployee'):
                usr = Employee(
                    user = User(
                        login = request.form.get('login'),
                        unhashed_password = request.form.get('password'),
                        isEmployee = True
                    ), 
                    email = request.form.get('email'),
                    isAdmin = 'on' == request.form.get('isAdmin'),
                    isOwner = 'on' == request.form.get('isOwner'),
                    isManager = 'on' == request.form.get('isManager'),
                    hotel_id = request.form.get('hotel')
                )
            else:
                usr = Customer(
                    user = User(
                        login = request.form.get('login'),
                        unhashed_password = request.form.get('password')
                    ), 
                    email = request.form.get('email')
                )
            db.session.add(usr)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Nastala chyba při vytváření nového účtu. Opakujte akci.')
        return redirect(url_for('dash.user_index'))





@dash.route('/dashboard/hotels', methods=['GET', 'POST'])
@login_required
def hotel_index():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        # this is create new hotel
        try:
            if 'picture' not in request.files:
                flash('No file part.')
                return redirect(request.url)
            file = request.files['picture']
            if file.filename == '':
                flash('No selected file.')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/css/img', filename))

            tmp = Hotel(
                name = request.form.get('name'),
                address = request.form.get('address'),
                description = request.form.get('description'),
                picture = file.filename
            )
            db.session.add(tmp)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Nastala chyba. Zkuste opakovat akci.')
        return redirect(url_for('dash.hotel_index'))
    else:
        # render the page (threre are no filters in hotels page)
        context = {
            'hotels': Hotel.query.all(),
            'occup_rooms': Room.query.outerjoin(Visit, Room.visits).filter(Visit.visit_type=='NOW').all(),
        }
        return render_template('dashboard_hotels.html', **context)

@dash.route('/dashboard/hotels/update', methods=['POST'])
@login_required
def hotel_update():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        obj = Hotel.query.filter_by(id=request.form.get('old_id')).first()
        try:
            obj.name = request.form.get('name')
            obj.address = request.form.get('address')
            obj.description = request.form.get('description')
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.hotel_index'))

@dash.route('/dashboard/hotels/delete', methods=['POST'])
@login_required
def hotel_delete():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            hotel = Hotel.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(hotel)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.hotel_index'))








@dash.route('/dashboard/room_index', methods=['POST', 'GET'])
@login_required
def room_index():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            #filter setting
            hotel_id = request.form.get('hotel')
            context = {
                'selected_h': hotel_id,
                'hotels': Hotel.query.all(),
                'rooms': Room.query.filter_by(hotel_id=hotel_id).order_by(Room.number.desc()).all(),
                'occup_rooms': Room.query.outerjoin(Visit, Room.visits).filter(Visit.visit_type=='NOW').all()
            }
            resp = make_response(render_template('dashboard_users.html', **context))
            resp.set_cookie('selected_hotel', hotel_id)
            resp.headers['location'] = url_for('dash.room_index')
            return resp, 302

        else:
            selected_hotel = request.cookies.get('selected_hotel')
            if not selected_hotel:
                selected_hotel = Hotel.query.first().id
            context = {
                'selected_h': selected_hotel,
                'hotels': Hotel.query.all(),
                'rooms': Room.query.filter_by(hotel_id=selected_hotel).order_by(Room.number.desc()).all(),
                'occup_rooms': Room.query.outerjoin(Visit, Room.visits).filter(Visit.visit_type=='NOW').all()
            }
            return render_template('dashboard_rooms.html', **context)

@dash.route('/dashboard/room_create', methods=['POST'])
@login_required
def room_create():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        print(request.form)
        try:
            temp = Room(
                number = request.form.get('number'),
                night_price = request.form.get('price'),
                room_type = request.form.get('type'),
                number_of_beds = request.form.get('beds'),
                hotel_id = request.form.get('hotel')
            )
            db.session.add(temp)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Zkuste to znovu.")
        return redirect(url_for('dash.room_index'))

@dash.route('/dashboard/room_update', methods=['POST'])
@login_required
def room_update():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        obj = Room.query.filter_by(id=request.form.get('old_id')).first()
        try:
            obj.number = request.form.get('number')
            obj.number_of_beds = request.form.get('beds')
            obj.night_price = request.form.get('price')
            obj.room_type = request.form.get('type')
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.room_index'))

@dash.route('/dashboard/room_delete', methods=['POST'])
@login_required
def room_delete():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            room = Room.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(room)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.room_index'))


@dash.route('/dashboard/reservation', methods=['GET', 'POST'])
@login_required
def reservation_index():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #handle search request -> set cookie and redirect to the main reservation page
        reservation_filter = request.form['reservation_filter']
        if (reservation_filter):
            reservations = Reservation.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Reservation.query.all()
        context = {
            'reservations': reservations
        }
        resp = make_response(render_template('dashboard_reservation.html', **context))
        resp.set_cookie('filter', reservation_filter)
        resp.headers['location'] = url_for('dash.reservation_index') 
        return resp, 302
    else:
        # main user page (apply search results filter if any)
        reservation_filter = request.cookies.get('filter')
        if (reservation_filter):
            reservations = Reservation.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Reservation.query.all()
        context = {
            'reservations' : reservations,
            'filter' : reservation_filter
        }
        return render_template('dashboard_reservation.html', **context)

@dash.route('/dashboard/reservation/update', methods=['POST'])
@login_required
def reservation_update():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        obj = Reservation.query.outerjoin(Visit).filter(Visit.id == request.form.get('id')).first()
        try:
            obj.is_paid_princ = 'on' == request.form.get('isPaidPrinc')
            obj.is_paid_visit = 'on' == request.form.get('isPaid')
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.reservation_index'))



@dash.route('/dashboard/reservation/checkin', methods=['POST'])
@login_required
def reservation_checkin():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            visit = Visit.query.filter_by(id=request.form.get('id')).first()
            to_del = visit.reservation
            to_add = Ongoing(
                visit = visit,
                is_paid_visit = to_del.is_paid_visit,
                key_customer = True
            )
            visit.visit_type = 'NOW'
            to_del.visit_id = 0
            db.session.add(to_add)
            db.session.commit()
            db.session.delete(to_del)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.reservation_index'))

@dash.route('/dashboard/reservation/delete', methods=['POST'])
@login_required
def reservation_delete():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            visit = Visit.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(visit)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.reservation_index'))









@dash.route('/dashboard/running', methods=['GET', 'POST'])
@login_required
def running_index():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #handle search request -> set cookie and redirect to the main reservation page
        reservation_filter = request.form['reservation_filter']
        if (reservation_filter):
            reservations = Ongoing.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Ongoing.query.all()
        context = {
            'reservations': reservations
        }
        resp = make_response(render_template('dashboard_running.html', **context))
        resp.set_cookie('filter', reservation_filter)
        resp.headers['location'] = url_for('dash.running_index') 
        return resp, 302
    else:
        # main user page (apply search results filter if any)
        reservation_filter = request.cookies.get('filter')
        if (reservation_filter):
            reservations = Ongoing.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Ongoing.query.all()
        context = {
            'reservations' : reservations,
            'filter' : reservation_filter
        }
        return render_template('dashboard_running.html', **context)

@dash.route('/dashboard/running/delete', methods=['POST'])
@login_required
def running_delete():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            visit = Visit.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(visit)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.running_index'))

@dash.route('/dashboard/running/update', methods=['POST'])
@login_required
def running_update():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        obj = Ongoing.query.outerjoin(Visit).filter(Visit.id == request.form.get('id')).first()
        try:
            obj.key_customer = 'on' == request.form.get('key')
            obj.is_paid_visit = 'on' == request.form.get('isPaid')
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.running_index'))

@dash.route('/dashboard/reservation/checkout', methods=['POST'])
@login_required
def running_checkout():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            visit = Visit.query.filter_by(id=request.form.get('id')).first()
            to_del = visit.ongoing
            to_add = Past(
                visit = visit
            )
            visit.visit_type = 'PAS'
            to_del.visit_id = 0
            db.session.add(to_add)
            db.session.commit()
            db.session.delete(to_del)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.running_index'))









@dash.route('/dashboard/ended', methods=['GET', 'POST'])
@login_required
def ended_index():
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #handle search request -> set cookie and redirect to the main reservation page
        reservation_filter = request.form['reservation_filter']
        if (reservation_filter):
            reservations = Past.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Past.query.all()
        context = {
            'reservations': reservations
        }
        resp = make_response(render_template('dashboard_ended.html', **context))
        resp.set_cookie('filter', reservation_filter)
        resp.headers['location'] = url_for('dash.ended_index') 
        return resp, 302
    else:
        # main user page (apply search results filter if any)
        reservation_filter = request.cookies.get('filter')
        if (reservation_filter):
            reservations = Past.query.outerjoin(Visit).filter(Visit.customer_id.contains(reservation_filter)).all()
        else:
            reservations = Past.query.all()
        context = {
            'reservations' : reservations,
            'filter' : reservation_filter
        }
        return render_template('dashboard_ended.html', **context)

@dash.route('/dashboard/ended/delete', methods=['POST'])
@login_required
def ended_delete():
    print(request.form)
    if not current_user.isEmployee:
        return redirect(url_for('main.index'))
    else:
        try:
            visit = Visit.query.filter_by(id=request.form.get('id')).first()
            db.session.delete(visit)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Něco se pokazilo. Opakujte akci.")
        return redirect(url_for('dash.ended_index'))