from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import Users
from blueprints import db, app, internal_required
from sqlalchemy import desc
import hashlib
import uuid

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class User(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status_internal', location='json', type=bool, default=True)
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(args['username'], args['phone_number'], hash_pass, salt, args['status_internal'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @internal_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims["id"])
        app.logger.debug('DEBUG : %s', qry)
        return marshal(qry, Users.response_fields), 200

    @internal_required
    def patch(self):
        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])

        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', location='json')
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        if args['phone_number'] is not None:
            user.phone_number = args['phone_number']
        
        if args['password'] is not None:
            salt = uuid.uuid4().hex
            encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()

            user.password = hash_pass
            user.salt = salt
            
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}


class UserAdmin(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    # @admin_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            app.logger.debug('DEBUG : id tidak ada')
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        app.logger.debug('DEBUG : data telah terhapus')

        return {'status': 'DELETED'}, 200

    # @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('phone_number'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp'] - args['rp'])

        qry = Users.query

        if args['orderby'] is not None:
            if args['orderby'] == 'phone_number':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.id))
                else:
                    qry = qry.order_by(Users.id)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200

api.add_resource(UserAdmin,'/admin', '/admin/<id>')
api.add_resource(User, '')
