import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "db.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_key_123'
    
    if os.environ.get('RENDER'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/render/project/src/db.sqlite3'
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        MAIN_DIR = os.path.dirname(BASE_DIR)
        db_path = os.path.join(MAIN_DIR, DB_NAME)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    db.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

    return app