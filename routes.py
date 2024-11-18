# Файл для определения маршрутов приложения (сайта)
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.newforms import EditProfileForm


@app.route('/')
@app.route('/home')  # декоратор, который проверяет авторизацию пользователя перед отображением страницы
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # проверка прохождения аутентификации
        return redirect(url_for('home'))  # если да, отправляем на домашнюю страницу
    form = RegistrationForm()  # если нет, создаем объект класса form и будем эту форму использовать
    if form.validate_on_submit():  # проверяем нажатие кнопки
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # шифрование пароля
        # в переменную user заносим все значения полей
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')  # отрисовка страницы

# Маршрут для страницы входа, также обрабатываем методы GET и POST.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # запрос в БД о проверке почты
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # запрос в БД о проверке пароля
            login_user(user, remember=form.remember.data)  # проверка нажатия значка "запомни меня"
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')


# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Маршрут для отображения страницы аккаунта. Декоратор login_required требует, чтобы пользователь был авторизирован.
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Маршрут для изменения данных
@app.route('/edit-profile')
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Здесь вы можете обработать данные формы и обновить профиль пользователя
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Например, сохраните данные в базе данных

        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form)