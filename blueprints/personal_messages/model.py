from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class PersonalMessages(db.Model):
    __tablename__ = "personal_messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    message = db.Column(db.Text)
    # status_deleted = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id':fields.Integer,
        'user_id':fields.Integer,
        'conversation_id':fields.Integer,
        'message':fields.String,
        'created_at':fields.DateTime
        # 'status_deleted':fields.Boolean
    }
    
    def __init__(self, user_id, conversation_id, message):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.message = message
        # self.status_deleted = status_deleted
        
    def __repr__(self):
        return '<PersonalMessage %r>' % self.id