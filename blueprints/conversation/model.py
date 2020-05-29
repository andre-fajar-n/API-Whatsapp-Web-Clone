from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Conversations(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # status_deleted = db.Column(db.Boolean, nullable=False)
    personal_message = db.relationship('PersonalMessages', backref='conversations', lazy=True, uselist=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id':fields.Integer,
        'user1_id':fields.Integer,
        'user2_id':fields.Integer,
        # 'status_deleted':fields.Boolean
        'created_at':fields.DateTime
    }
    
    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
        # self.status_deleted = status_deleted
        
    def __repr__(self):
        return '<Conversation %r>' % self.id