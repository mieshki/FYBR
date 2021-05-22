from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='FYBR'
    )

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://FYBR:FYBR@127.0.0.1/FYBR'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # only for single usage. Remove it after first run
    from app import models
    with app.app_context():
        db.create_all()

    return app
