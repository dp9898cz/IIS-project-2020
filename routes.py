from flask import Blueprint, render_template, request, redirect, url_for

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
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')