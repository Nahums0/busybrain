# Standard Library imports
import logging
import os
from logging.handlers import RotatingFileHandler

# Core Flask imports
from flask import Flask
from flask_login import LoginManager

# Third-party imports

# App imports
from app.database import DatabaseManager
from config import config_manager
from app.mqtt import init_mqtt, set_mqtt_configuration


# Load extensions
login_manager = LoginManager()
db_manager = DatabaseManager()

def load_logs(app):
    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("app startup")
    return


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_manager[config_name])

    set_mqtt_configuration(app)
    init_mqtt(app)

    config_manager[config_name].init_app(app)

    login_manager.login_view = "routes.login"
    login_manager.init_app(app)

    db_manager.init_app(app)

    from app.routes import register_api_routes
    app = register_api_routes(app)

    if not app.debug and not app.testing:
        load_logs(app)

    return app