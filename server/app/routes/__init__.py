from flask import Flask
from .users import users_bp

def register_api_routes(app:Flask):
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app