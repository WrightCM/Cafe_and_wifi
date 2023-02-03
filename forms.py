from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SelectField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class Add(FlaskForm):
    name = StringField("Cafe's Name", validators=[DataRequired()])
    img_url = URLField("Image Url", validators=[DataRequired(), URL()])
    location_url = URLField("Cafe's Location", validators=[DataRequired(), URL()])
    rating = SelectField('Rating', choices=[("Ⅹ"), ("⭐☆☆☆☆"), ("⭐⭐☆☆☆"), ("⭐⭐⭐☆☆"), ("⭐⭐⭐⭐☆"), ("⭐⭐⭐⭐⭐")])
    description = CKEditorField("Description / Review")
    sumbit = SubmitField('Submit')

class Register(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class Login(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()