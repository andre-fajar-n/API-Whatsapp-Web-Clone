from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    status_internal = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'phone_number': fields.String,
        'password': fields.String,
        'status_internal': fields.Boolean,
    }

    jwt_client_fields = {
        'id': fields.Integer,
        'phone_number': fields.String,
        'status_internal': fields.Boolean,
    }

    def __init__(self, phone_number, password, salt, status_internal):
        self.phone_number = phone_number
        self.password = password
        self.salt = salt
        self.status_internal = status_internal

    def __repr__(self):
        return '<User %r>' % self.id
