from flask import render_template, flash,request
from app import app, bcrypt, db

from app.forms import RegisterForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = bcrypt.generate_password_hash(form.password.data)
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Congrats,registration success', category='success')

    return render_template('register.html', form=form)
