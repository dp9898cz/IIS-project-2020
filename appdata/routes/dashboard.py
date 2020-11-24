from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dash_index():
    if not current_user.isEmployee:
        #user with no rights cant enter -> redirect
        return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_index.html')
@dash.route('/users', methods=['GET'])
def users():
    if not current_user.isEmployee:
         return redirect(url_for('main.index'))
    else:
        return render_template('dashboard_users.html')
@dash.route('/hotels', methods=['GET'])
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
