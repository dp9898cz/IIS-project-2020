from flask import Blueprint, render_template, redirect, url_for, request, make_response
from flask_login import login_required, current_user

from appdata.models import User, Employee, Customer
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
    if not current_user.isEmployee:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    elif request.method == 'POST':
        #user_filter = request.form
        users = User.query.all()
        resp = make_response(render_template('dashboard_users.html', users=users))
        resp.set_cookie('filter', 'aaaaaaaaaaa')
        return resp
    else:
        user_filter = request.cookies.get('filter')
        print(user_filter)
        users = User.query.all()
        return render_template('dashboard_users.html', users=users)

@dash.route('/dashboard/users/update', methods=['POST'])
@csrf.exempt
@login_required
def update_user():
    print(request.form)