from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'input_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)  # создание объекта SQLAlchemy, подключение к приложению
bcrypt = Bcrypt(app)  # создание объекта класса Bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Модуль будет перенаправлять пользователя на маршрут, n/
# который мы указываем (на авторизацию)

from app import routes
# теперь в файле прописаны все конфигурационные настройки
