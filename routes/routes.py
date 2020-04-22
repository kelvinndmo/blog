from flask import render_template, url_for, flash, redirect, request
from app.app import app,db, bcrypt
from forms.forms import LoginForm, RegistrationForm
from models.models import User
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {"author":"novak","date_posted":"Aug_7, 2020"}
]

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
        
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("login unsuccessfull", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/account")
@login_required
def account():
    img_file = url_for('static', filename='img/'+current_user.image_file)
    print(img_file)
    return render_template('account.html', img_file=img_file)