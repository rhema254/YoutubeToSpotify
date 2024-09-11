from flask import Flask 
from Server.config import DevConfig, ProdConfig

def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
    