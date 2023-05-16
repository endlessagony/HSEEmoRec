from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager



db = SQLAlchemy()
DB_NAME = "database.db"
USERSDATA_DIR = "usersdata/"
USERSDATA_PATH = USERSDATA_DIR + 'usersdata.csv'
ANALYSIS_DIR = 'analysis/'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hserecemo'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)
    create_usersdata()
    create_analysis_dir()

    return app


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database was created')

def create_usersdata():
    if not os.path.exists(USERSDATA_DIR):
        os.mkdir(USERSDATA_DIR)
        with open(USERSDATA_PATH, 'w') as file:
            file.write('id,user_email,position,sex,age,date,weekday,is_weekend,emotion\n')

def create_analysis_dir():
    if not os.path.exists(ANALYSIS_DIR):
        os.mkdir(ANALYSIS_DIR)