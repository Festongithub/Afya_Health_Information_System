from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from uuid import uuid4
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from AfyaBoraApp import db
from werkzeug.security import generate_password_hash, check_password_hash

# Define the enrollment table for the many-to-many relationship between Client and HealthProgram
enrollment = db.Table(
    'enrollment',
    db.Column('client_id', sa.String(36), db.ForeignKey('client.id'), primary_key=True),
    db.Column('program_id', sa.String(36), db.ForeignKey('health_program.id'), primary_key=True)
)

class HealthProgram(db.Model):
    __tablename__ = 'health_program'  # Explicit table name for clarity

    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid4()))
    programname: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    clients: so.Mapped[List["Client"]] = so.relationship(
        "Client", secondary=enrollment, back_populates="enrolled_programs"
    )

    def __repr__(self):
        return f'<HealthProgram {self.programname}>'

class Doctor(db.Model):
    __tablename__ = 'doctor'

    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid4()))
    doctorname: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    
    def set_password(self, password):
        """
        set new password for the client
        """
        self.password_hash  = generate_password_hash(password)


    def check_password(self, password):
        """
        verify password of the client
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Doctor {self.doctorname}>'



class Client(UserMixin, db.Model):
    __tablename__ = 'client'

    id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid4()))
    clientname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    gender: so.Mapped[str] = so.mapped_column(sa.String(10), index=True)  # Removed unique=True
    enrolled_programs: so.Mapped[List["HealthProgram"]] = so.relationship(
        "HealthProgram", secondary=enrollment, back_populates="clients"
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        """
        set new password for the client
        """
        self.password_hash  = generate_password_hash(password)


    def check_password(self, password):
        """
        verify password of the client
        """
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return f'<User {self.clientname}>'
    
    @login.user_loader
    def load_client(id):
        return db.session.get(Client, int(id))


# Health Management System
class HealthSystem:
    @staticmethod
    def build_program(name, description):
        if not name or len(name.strip()) == 0:
            raise ValueError("Program name cannot be empty")

        program = HealthProgram(name=name.strip(), description=description)
        db.session.add(program)
        db.session.commit()
        logging.info(f"Program created: {name}")
        return program

    @staticmethod
    def client_register(name, age, gender):
        if not name or age < 0:
            raise ValueError("Invalid client details")
        client = Client(name=name.strip(), age=age, gender=gender)
        db.session.add(client)
        db.session.commit()
        logging.info(f"client registered: {name}")
        return client

    @staticmethod
    def client_enrollment(client_id, program_id):
        client = Client.query.get(client_id)
        program = HealthProgram.query.get(program_id)
        if not client or not program:
            raise ValueError("Client or program not found")
        if program not in client.enrolled_programs:
            client.enrolled_programs.append(program)
            db.session.commit()
            logging.info(f"Client {client.name} enrolled in {program.name}")
        return client

    @staticmethod
    def search_clients(query):
        return Client.query.filter(Client.name.ilike(f"%{query}%")).all()

    @staticmethod
    def get_client_profile(client_id):
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Client not found")
        return client
