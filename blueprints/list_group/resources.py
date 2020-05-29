from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import ListGroup
from blueprints.user.model import Users
from blueprints.member_group.model import MemberGroup
from blueprints import db, app, internal_required
from sqlalchemy import desc

bp_list_group = Blueprint('list_group', __name__)
api = Api(bp_list_group)

class ListGroupResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    @internal_required
    def post(self):
        claims = get_jwt_claims()
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        args = parser.parse_args()
        
        # menambah data group ke tabel
        group = ListGroup(args['name'])
        db.session.add(group)
        db.session.commit()
        
        # menambah anggota group(pembuat group) ke tabel
        member_group = MemberGroup(group.id, claims['id'])
        db.session.add(member_group)
        db.session.commit()
        
        # ambil data user yang membuat group
        user = Users.query.get(claims['id'])
        
        # memasukkan data user ke response
        user_marshal = marshal(user, Users.response_fields)
        group_marshal = marshal(group, ListGroup.response_fields)
        group_marshal['created_by'] = user_marshal
        
        app.logger.debug('DEBUG: %s', group_marshal)
        return group_marshal, 200
    
api.add_resource(ListGroupResource, '')