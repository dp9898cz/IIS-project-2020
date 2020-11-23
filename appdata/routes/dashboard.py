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