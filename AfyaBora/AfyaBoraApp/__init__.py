from flask import Flask
import config
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from AfyaBoraApp import routes, models

def init_shell():
    from AfyaBoraApp import app, db
    from AfyaBoraApp.models import Client, HealthProgram, Doctor
    app.app_context().push()
    return app, db, Client, HealthProgram, Doctor