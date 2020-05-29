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
        parser.add_argument('group_chat_id', location='json', required=True)
        parser.add_argument('message', location='json')
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
    
    @internal_required
    def get(self):
        claims = get_jwt_claims()
        
        # memfilter group yang user sebagai anggotanya
        group_by_user = MemberGroup.query.filter_by(user_id=claims['id'])
        
        # memasukkan list group ke dalam array
        list_group = []
        for group in group_by_user:
            detail_group = ListGroup.query.get(group.group_chat_id)
            marshal_detail_group = marshal(detail_group, ListGroup.response_fields)
            
            # memfilter message berdasarkan group
            message_group = MessageGroup.query.filter_by(group_chat_id=group.id)
            
            # memasukkan pesan terakhir group
            last_message_group = message_group.order_by(desc(MessageGroup.created_at)).first()
            marshal_last_message_group = marshal(last_message_group, MessageGroup.response_fields)
            marshal_detail_group['last_chat'] = marshal_last_message_group
            
            # memasukkan tiap message ke detail masing2 group
            all_message = []
            for message in message_group:
                # mendapatkan data user yang mengirim pesan
                user = Users.query.get(message.user_id)
                marshal_user = marshal(user, Users.response_fields)
                
                marshal_message = marshal(message, MessageGroup.response_fields)
                marshal_message['user'] = marshal_user
                all_message.append(marshal_message)
            marshal_detail_group['all_message'] = all_message
            
            list_group.append(marshal_detail_group)
            
        app.logger.debug('DEBUG: %s', list_group)
        return list_group, 200
    
api.add_resource(MessageGroupResource, '')