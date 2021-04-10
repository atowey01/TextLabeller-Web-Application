from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from text_labeller.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from text_labeller.users.routes import users
    from text_labeller.create_projects.routes import create_projects
    from text_labeller.label_data.routes import label_data
    from text_labeller.view_data.routes import view_data_blueprint
    from text_labeller.main.routes import main
    from text_labeller.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(create_projects)
    app.register_blueprint(label_data)
    app.register_blueprint(view_data_blueprint)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
