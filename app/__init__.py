from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
DB_NAME = 'FYBR'
DB_PASSWORD = 'FYBR'


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='FYBR'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #db = SQLAlchemy.init_app(app)
    #db.session

    return app
