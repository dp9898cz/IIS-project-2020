from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from extensions import db
from models import Users, Hotel

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        unhashed_pass = request.form['password']
        
        user = Users(
            name = name, 
            unhashed_password = unhashed_pass, 
            isAdmin = True
        )

        db.session.add(user)
        try:
            db.session.commit()
        except:
            print("user already exists")
            #todo error handle
            return redirect(url_for('main.index'))

        #login the user
        login_user(user)

        return redirect(url_for('main.index')) #todo? maybe redirect to the profile?

    return render_template('register.html')

@main.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    passwrd = request.form['password']
    user = Users.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, passwrd):
        pass
        #todo error
    else:
        login_user(user)
        return redirect(url_for('main.index'))

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

