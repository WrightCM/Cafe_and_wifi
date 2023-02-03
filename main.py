from flask import Flask, render_template, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
from datetime import datetime
from forms import *

"#C46C48"
"#20273A"
"B4BFAD"
"5E6F90"
"374045"
"D89216"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Cafes(db.Model):
    __tablename__ = 'cafes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    location = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship('Users', back_populates='posts')


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    posts = relationship('Cafes', back_populates='author')
    rol = db.Column(db.Integer)


app.app_context().push()
db.create_all()


def admin_only(f):
    def wrapped_function(*args, **kwargs):
        if current_user.rol != 1:
            return abort(403)
        return f(*args, **kwargs)

    return wrapped_function


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def homepage():
    cafes = Cafes.query.all()
    return render_template("index.html", current_user=current_user, cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    form = Add()
    if form.validate_on_submit():
        try:
            new_post = Cafes(
                name=form.name.data,
                img_url=form.img_url.data,
                location=form.location_url.data,
                rating=form.rating.data,
                description=form.description.data,
                author=current_user,
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('homepage'))
        except:
            flash('That cafe is already in our database.')
    return render_template('add.html', form=form, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        username = Users.query.filter_by(name=form.name.data).first()
        email = Users.query.filter_by(email=form.email.data).first()
        if not email:
            if not username:
                password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
                new_user = Users(
                    name=form.name.data,
                    email=form.email.data,
                    password=password,
                    rol=0
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('homepage'))
            else:
                flash('That username has already been taken,')
        else:
            flash(
                'That account already exists. Log in instead.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            password = check_password_hash(user.password, form.password.data)
            if password:
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                flash("That's the wrong password.")
        else:
            flash("That email account doesn't exists.")
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/delete/<int:card_id>')
def delete(card_id):
    card = Cafes.query.filter_by(id=card_id).first()
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/edit/<int:card_id>', methods=['POST', 'GET'])
def edit(card_id):
    card = Cafes.query.filter_by(id=card_id).first()
    form = Add(
        name= card.name,
        img_url= card.img_url,
        location_url = card.location,
        rating = card.rating,
        description = card.description
    )
    if form.validate_on_submit():
        card.name = form.name.data
        card.img_url = form.img_url.data
        card.location = form.location_url.data
        card.rating = form.rating.data
        card.description = form.description.data
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('add.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
