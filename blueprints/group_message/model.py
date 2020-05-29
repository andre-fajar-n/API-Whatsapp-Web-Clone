from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationships, backref
from sqlalchemy import ForeignKey

class MessageGroup(db.Model):
    __tablename__ = "message_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_chat_id = db.Column(db.Integer, db.ForeignKey('list_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id':fields.Integer,
        'group_chat_id':fields.Integer,
        'user_id':fields.Integer,
        'message':fields.String,
        'created_at':fields.DateTime,
    }
    
    def __init__(self, group_chat_id, user_id, message):
        self.group_chat_id = group_chat_id
        self.user_id = user_id
        self.message = message
        
    def __repr__(self):
        return '<GroupMessage %r>' % self.id