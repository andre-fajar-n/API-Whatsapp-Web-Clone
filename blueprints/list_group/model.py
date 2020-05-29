from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationships, backref
from sqlalchemy import ForeignKey

class ListGroup(db.Model):
    __tablename__ = "list_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id':fields.Integer,
        'name':fields.String,
        'created_at':fields.DateTime,
    }
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<ListGroup %r>' % self.id