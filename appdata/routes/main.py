from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from appdata.extensions import db
from appdata.models import Users, Hotel
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
    print(form.email)
    if form.validate_on_submit():
        print("success")
        return render_template('index.html', registerForm=form, openWindow=0)
    else:
        print("failed")
        return render_template('index.html', registerForm=form, openWindow=1)

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

@main.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.login.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            #todo wrong password error
            context = {
                'registerForm': RegisterForm(),
                'loginForm': form,
                'openWindow': 1
            }
            return render_template('index.html', **context)
        else:
            #successfully logged in
            login_user(user)
            return redirect(url_for("main.index"))
    else:
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
                'openWindow': 1
            }
    return render_template('sport.html', **context)

#o služby-personal -template
@main.route('/personal', methods=['GET'])
def personal():
    context = {
                'registerForm': RegisterForm(),
                'loginForm': LoginForm(),
                'openWindow': 1
            }
    return render_template('personal.html', **context)

