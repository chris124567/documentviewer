# init.py

# flask
from flask_admin import Admin
from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['WEBSITE_NAME'] = "DocumentViewer"
    app.config['WEBSITE_HOST'] = "localhost:5000"

    app.config['SECRET_KEY'] = "ktGSOu1QLcc1WBQDxzTK"

    # TODO: use actual database backend (postgres, ...)
    # sql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config[
        'SEND_FILE_MAX_AGE_DEFAULT'] = 0  # NO CACHE, at least for development
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # wasteful feature

    app.config['UPLOAD_FOLDER'] = "data"

    admin = Admin(
        app,
        name=app.config['WEBSITE_NAME'],
        template_mode='bootstrap3',
        url='/admin')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # login page
    # login_manager.session_protection = 'strong'
    # ^ prevents "remember me" button from working so is disabled

    login_manager.init_app(app)

    from .models import User, File
    # add user database to admin page
    admin.add_view(ModelView(User, db.session))
    # add file database to admin page
    admin.add_view(ModelView(File, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it
        # in the query for the user
        return User.query.get(int(user_id))

    # so it figures out current app context
    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint)

    from .download import download as download_blueprint
    app.register_blueprint(download_blueprint)

    from .document import document as document_blueprint
    app.register_blueprint(document_blueprint)

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from .static import static as static_blueprint
    app.register_blueprint(static_blueprint)

    return app
