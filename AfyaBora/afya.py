import sqlalchemy as sa
import sqlalchemy.orm as so
from AfyaBoraApp import app, db
from AfyaBoraApp.models import HealthProgram, Client, Doctor

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'db': db, 'HealthProgram': HealthProgram, 'Client': Client, 'Doctor': Doctor}
