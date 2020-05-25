from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from blueprints.user.model import Users
import hashlib

from blueprints import internal_required

bp_token = Blueprint('token', __name__)
api = Api(bp_token)


class CreateTokenResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        qry_user = Users.query.filter_by(phone_number=args['phone_number']).first()

        if qry_user is not None:
            client_salt = qry_user.salt
            encoded = ('%s%s' % (args['password'], client_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_user.password and qry_user.phone_number == args['phone_number']:
                qry_user = marshal(qry_user, Users.jwt_client_fields)
                token = create_access_token(identity=args['phone_number'], user_claims=qry_user)
                return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404


class RefreshTokenResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @internal_required
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=claims)
        return {'token': token}, 200


api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
