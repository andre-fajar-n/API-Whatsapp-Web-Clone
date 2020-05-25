import pytest
import json
import logging

from blueprints import app

from flask import Flask, request

from app import cache, logging

from blueprints import db

import hashlib, uuid

# from blueprints.client.model import Clients
from blueprints.user.model import Users

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    # create the database and the database table
    db.create_all()
    
    salt = uuid.uuid4().hex
    encoded = ('%s%s' % ("password", salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encoded).hexdigest()
    # insert user data
    # client_internal = Clients(client_key="internal", client_secret=hash_pass, status="True", salt=salt)
    # client_noninternal = Clients(client_key="noninternal", client_secret=hash_pass, status="False", salt=salt)
    # db.session.add(client_internal)
    # db.session.add(client_noninternal)
    # db.session.commit()
    
    user_internal = Users(phone_number='085735950340',password=hash_pass,salt= salt,status_internal= True)
    user_noninternal = Users(phone_number='085735950341',password=hash_pass,salt= salt,status_internal= False)
    db.session.add(user_internal)
    db.session.add(user_noninternal)
    db.session.commit()
    
    yield db
    
    db.drop_all()

def create_token_internal():
    token = cache.get('test-token')
    if token is None:
    # prepare request input
        data = {
            'phone_number': '085735950340',
            'password': 'password',
        }
        
        # do request 
        req = call_client(request)
        res = req.get('/login',query_string=data,content_type='application/json')
        
        # store response
        res_json = json.loads(res.data)
        
        app.logger.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200
        
        # save token into cache
        cache.set('test-token', res_json['token'], timeout=60)
        
        # return, because it usefull for other test
        return res_json['token']
    else:
        return token
    
def create_token_noninternal():
    token = cache.get('test-token')
    if token is None:
    # prepare request input
        data = {
            'phone_number': '085735950341',
            'password': 'password',
        }
        
        # do request 
        req = call_client(request)
        res = req.get('/login',query_string=data,content_type='application/json')
        
        # store response
        res_json = json.loads(res.data)
        
        app.logger.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 403
        
        # save token into cache
        cache.set('test-token', res_json['token'], timeout=60)
        
        # return, because it usefull for other test
        return res_json['token']
    else:
        return token
