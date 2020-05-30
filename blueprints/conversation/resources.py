from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import Conversations
from blueprints.user.model import Users
from blueprints.personal_messages.model import PersonalMessages
from blueprints import db, app, internal_required
from sqlalchemy import desc, or_

bp_conversation = Blueprint('conversation', __name__)
api = Api(bp_conversation)

class ConversationResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    def delete(self, id):
        qry = PersonalMessages.query.get(id)
        if qry is None:
            app.logger.debug('DEBUG : id tidak ada')
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        app.logger.debug('DEBUG : data telah terhapus')

        return {'status': 'DELETED'}, 200
    
api.add_resource(ConversationResource, '', '/<id>')