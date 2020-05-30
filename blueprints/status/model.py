from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey

class StatusWA(db.Model):
    __tablename__ = "status_wa"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'content': fields.String,
        'image': fields.String,
        'created_at': fields.DateTime
    }
    
    def __init__(self, user_id, content, image):
        self.user_id = user_id
        self.content = content
        self.image = image
        
    def __repr__(self):
        return '<StatusWA %r>' % self.id