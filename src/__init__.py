"""__init__.py"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
from flask_login import LoginManager

passenger_login_manager = LoginManager()
driver_login_manager = LoginManager()
loginManager = LoginManager()

db_Name = "asambe.db"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_Name}"
    app.config["SECRET_KEY"] = "hehehehehe"

    # login manger conf
    passenger_login_manager.login_view = "passenger_auth.signin"

    # initializations
    db.init_app(app)

    passenger_login_manager.init_app(app)

    # Models
    from .models.passenger import Passenger
    from .models.driver import Driver
    from .models.location import Location
    from .models.vehicle import Vehicle

    # set up the loading all users by using different login managers
    @passenger_login_manager.user_loader
    def load_passenger(passenger_id):
        return Passenger.query.get(int(passenger_id))

    # @passenger_login_manager.user_loader
    # def load_user(user_id):
    #    # Check if the user is a passenger or driver
    #    if Passenger.query.get(user_id):
    #        return Passenger.query.get(user_id)
    #    elif Driver.query.get(user_id):
    #        return Driver.query.get(user_id)
    #    else:
    #        return None

    # create the database
    create_database(app)

    # Registering blueprints
    from .routes.passenger.auth import passenger_auth
    from .routes.passenger.views import passenger_views

    app.register_blueprint(passenger_auth)
    app.register_blueprint(passenger_views)

    return app


def create_database(app):
    if not path.exists(f"instance/{db_Name}"):
        with app.app_context():
            db.create_all()
