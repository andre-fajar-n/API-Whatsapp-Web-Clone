from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
from blueprints import db, app, internal_required
from sqlalchemy import desc

from .model import MemberGroup
from blueprints.list_group.model import ListGroup
from blueprints.user.model import Users

bp_member_group = Blueprint('member_group', __name__)
api = Api(bp_member_group)

class MemberGroupResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    @internal_required
    def post(self):
        claims = get_jwt_claims()
        
        parser = reqparse.RequestParser()
        parser.add_argument('group_chat_id', location='json', required=True)
        parser.add_argument('user_id', location='json', required=True)
        args = parser.parse_args()
        
        # cek group sudah ada atau belum
        group = ListGroup.query.get(args['group_chat_id'])
        if group is None:
            app.logger.debug('DEBUG: Group not found')
            return {'status':'Group not found'}, 404
        
        # cek user sudah jadi anggota belum
        current_member_group = MemberGroup.query.filter_by(group_chat_id=args['group_chat_id'])
        current_member_group = current_member_group.filter_by(user_id=args['user_id']).first()
        if current_member_group is not None:
            app.logger.debug('DEBUG: User have been member of group')
            return {'status':'User have been member of group'}, 403
        
        member_group = MemberGroup(args['group_chat_id'], args['user_id'])
        db.session.add(member_group)
        db.session.commit()
        
        app.logger.debug('DEBUG: Success add %s', member_group)
        return marshal(member_group, MemberGroup.response_fields), 200
    
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group_chat_id', location='json', required=True)
        args = parser.parse_args()
        
        group = ListGroup.query.get(args['group_chat_id'])
        if group is None:
            app.logger.debug('DEBUG: Group not found')
            return {'status':'Group not found'}, 404
        
        # menambahkan anggota group ke response
        member_groups = MemberGroup.query.filter_by(group_chat_id=args['group_chat_id'])
        member = []
        for member_group in member_groups:
            user = Users.query.get(member_group.user_id)
            marshal_user = marshal(user, Users.response_fields)
            member.append(marshal_user)
            
        group_marshal = marshal(group, ListGroup.response_fields)
        group_marshal['member'] = member
        
        app.logger.debug('DEBUG: %s', group_marshal)
        return group_marshal, 200
    
api.add_resource(MemberGroupResource, '')