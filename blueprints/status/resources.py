from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
from blueprints import db, app, internal_required
from sqlalchemy import desc, or_
from datetime import datetime
import werkzeug
import os
import uuid

from .model import StatusWA
from blueprints.user.model import Users

bp_status = Blueprint('status', __name__)
api = Api(bp_status)

class StatusResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    @internal_required
    def post(self):
        claims = get_jwt_claims()
        
        parser = reqparse.RequestParser()
        parser.add_argument('content', location='form')
        parser.add_argument('image', location='files', type=werkzeug.datastructures.FileStorage, default='')
        args = parser.parse_args()
        
        UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

        image_status = args['image']

        if image_status:
            randomstr = uuid.uuid4().hex  # get random string to image filename
            filename = randomstr+'_'+image_status.filename
            image_status.save(os.path.join("."+UPLOAD_FOLDER, filename))
            img_path = UPLOAD_FOLDER.replace('./', '/')+'/'+filename
        else:
            filename = ''
        
        status = StatusWA(claims['id'], args['content'], filename)
        db.session.add(status)
        db.session.commit()
        
        app.logger.debug('DEBUG: %s', status)
        return marshal(status, StatusWA.response_fields), 200
    
    @internal_required
    def get(self):
        claims = get_jwt_claims()
        
        # ambil data user selain yang sedang login
        users = Users.query.filter(Users.id != claims['id'])
        list_user = []
        for user in users:
            marshal_user = marshal(user, Users.response_fields)
            
            # filter user yang punya status
            status = StatusWA.query.filter_by(user_id=user.id)
            if status.first() is not None:
                # memasukkan status terakhir
                last_status = status.order_by(desc(StatusWA.created_at)).first()
                marshal_user['last_status'] = marshal(last_status, StatusWA.response_fields)
                
                # memasukkan semua status yang dibuat
                list_status = []
                for status_user in status:
                    list_status.append(marshal(status_user, StatusWA.response_fields))
                marshal_user['all_status'] = list_status
            
                list_user.append(marshal_user)
            
        app.logger.debug('DEBUG: %s', list_user)
        return list_user, 200
    
class ListStatusResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    def get(self, id):
        list_status = StatusWA.query.filter_by(user_id=id)
        
        all_status = []
        for status in list_status:
            all_status.append(marshal(status, StatusWA.response_fields))
            
        app.logger.debug('DEBUG: %s', all_status)
        return all_status, 200
        
api.add_resource(StatusResource, '')
api.add_resource(ListStatusResource, '/<id>')