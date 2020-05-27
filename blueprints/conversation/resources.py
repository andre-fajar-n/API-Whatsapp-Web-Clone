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
    
    @internal_required
    def get(self):
        claims = get_jwt_claims()
        
        # filter tabel conversation dari user yang login
        conversations = Conversations.query.filter(or_(Conversations.user1_id.like(claims['id']), Conversations.user2_id.like(claims['id'])))
        
        list_conversation = []
        for conversation in conversations:
            personal_messages = PersonalMessages.query.filter_by(conversation_id=conversation.id)
            personal_messages = personal_messages.order_by(desc(PersonalMessages.created_at)).first()
            marshal_personal_message = marshal(personal_messages, PersonalMessages.response_fields)
            
            marshal_conversation = marshal(conversation, Conversations.response_fields)
            
            marshal_conversation['last_chat'] = marshal_personal_message
            
            # memasukkan data lawan chat ke response
            if marshal_conversation['user1_id'] != claims['id']:
                user = Users.query.get(marshal_conversation['user1_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['data_user'] = marshal_user
                
            # memasukkan data lawan chat ke response
            if marshal_conversation['user2_id'] != claims['id']:
                user = Users.query.get(marshal_conversation['user2_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['data_user'] = marshal_user
                
            list_conversation.append(marshal_conversation)
            
        app.logger.debug('DEBUG: %s', list_conversation)
        return list_conversation, 200
    
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