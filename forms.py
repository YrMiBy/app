# Модуль создания и управления формами
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#Валидаторы. Валидатор EqualTo нужен для того, чтобы сравнивать значения в полях и узнавать, точно ли они одинаковые.
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):  # класс формы для регистрации
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])  # поля
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Повторение пароля
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


def validate_username(self, username): # для проверки наличия того же как введенное имени в базе
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('Такое имя уже существует.')  #raise используется для проверки исключений


def validate_email(self, email):  #  проверка наличия  почты
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Такая почта уже используется.')

class LoginForm(FlaskForm):  # класс для ввода заполненной формы
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')


