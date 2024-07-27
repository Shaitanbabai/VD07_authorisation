# Этот файл прописывает все декораторы с маршрутами на сайте
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt  # bcrypt - шифратор введенных паролей
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm


# Создаём маршрут для главной страницы.
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Создаём маршрут для страницы регистрации, обрабатываем методы GET и POST.
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если юзер зарегистрирован - перенаправляем на домашнюю страницу
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Если юзер не зарегистрирован - создаем объект формы регистрации
    form = RegistrationForm()
    if form.validate_on_submit():
        # Тут bcrypt шифрует пароль
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Создаем объект класса для сохранения данных в базу
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Добавляем пользователя в сессию и подтверждаем запись
        db.session.add(user)
        db.session.commit()
        # Подтверждаем завершение регистрации
        flash('Вы успешно зарегистрировались', 'success')
        # Возврат на страницу авторизации
        return redirect(url_for('login'))
    # Отрисовка страницы
    return render_template('register.html', form=form)


# Создаём маршрут для страницы входа, также обрабатываем методы GET и POST.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():  # проверяем, нажата ли кнопка
        # введены ли соответствующие данные
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Запоминаем юзера
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные', 'danger')
    return render_template('login.html', form=form)


# Создаём маршрут для выхода из аккаунта.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Создаём маршрут для отображения страницы аккаунта.
# Декоратор login_required требует, чтобы пользователь был авторизирован.
@app.route('/account')
@login_required
def account():
    # Получаем данные пользователя из базы данных
    user = User.query.get(current_user.id)
    return render_template('account.html', user=user)


@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_account.html',form=form)