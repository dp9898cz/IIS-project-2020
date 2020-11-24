from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response
from flask_login import login_required, current_user

from appdata.models import User, Employee, Customer, Hotel
from appdata.extensions import csrf

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dash_index():
    if not current_user.isEmployee:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    else:
        users = User.query.filter_by(isEmployee='1', login='admin').all()
        print(users)
        return render_template('dashboard_index.html')

@dash.route('/dashboard/users')
@csrf.exempt
@login_required
def user_index():
    if not current_user.employees.isAdmin:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #user_filter = request.form
        users = User.query.all()
        hotels = Hotel.query.all()
        resp = make_response(render_template('dashboard_users.html', hotels=hotels, users=users))
        resp.set_cookie('filter', 'aaaaaaaaaaa')
        return resp
    else:
        user_filter = request.cookies.get('filter')
        print(user_filter)
        users = User.query.all()
        hotels = Hotel.query.all()
        return render_template('dashboard_users.html', hotels=hotels, users=users)

@dash.route('/dashboard/users/update', methods=['POST'])
@csrf.exempt
@login_required
def update_user():
    print(request.form)
    old_user_obj = User.query.filter_by(id = request.form['old_id']).first()
    if (old_user_obj.login != request.form['login']):
        #changing the login -> have to check if its free
        temp = User.query.filter_by(login=request.form['login']).first()
        if temp != None:
            flash('Tento login už existuje. Použijte jiný.')
            return redirect(url_for('dash.user_index'))
    try:
        old_user_obj.login = request.form['login']
        if (old_user_obj.isEmployee):
            old_user_obj.employees.isAdmin = request.form['isAdmin']
            old_user_obj.employees.isOwner = request.form['isOwner']
            old_user_obj.employees.isManager = request.form['isManager']
            old_user_obj.employees.email = request.form['email']
            #todo hotel
        else:
            old_user_obj.customers.email = request.form['email']
    except:
        pass
    return redirect(url_for('dash.user_index'))
def hotels():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_hotels.html')
@dash.route('/rooms', methods=['GET'])
def rooms():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_rooms.html')
@dash.route('/reservation', methods=['GET'])
def reservation():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_reservation.html')
@dash.route('/running', methods=['GET'])
def running():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_running.html')
@dash.route('/ended', methods=['GET'])
def ended():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_ended.html')
