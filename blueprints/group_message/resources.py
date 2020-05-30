from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
from blueprints import db, app, internal_required
from sqlalchemy import desc

from .model import MessageGroup
from blueprints.list_group.model import ListGroup
from blueprints.member_group.model import MemberGroup
from blueprints.user.model import Users

bp_message_group = Blueprint('message_group', __name__)
api = Api(bp_message_group)

class MessageGroupResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    @internal_required
    def post(self):
        claims = get_jwt_claims()
        
        parser = reqparse.RequestParser()
        parser.add_argument('group_chat_id', location='args', required=True)
        parser.add_argument('message', location='args')
        args = parser.parse_args()
        
        # cek grup ada atau tidak
        group = ListGroup.query.get(args['group_chat_id'])
        if group is None:
            app.logger.debug('DEBUG: Group not found')
            return {'status':'Group not found'}, 404
        
        # cek user termasuk anggota atau bukan
        current_member_group = MemberGroup.query.filter_by(group_chat_id=args['group_chat_id'])
        current_member_group = current_member_group.filter_by(user_id=claims['id']).first()
        if current_member_group is None:
            app.logger.debug('DEBUG: User not a member of group')
            return {'status':'User not member of group'}, 403
        
        message_group = MessageGroup(args['group_chat_id'], claims['id'], args['message'])
        db.session.add(message_group)
        db.session.commit()
        
        app.logger.debug('DEBUG: Send a message success')
        return marshal(message_group, MessageGroup.response_fields), 200
    
api.add_resource(MessageGroupResource, '')