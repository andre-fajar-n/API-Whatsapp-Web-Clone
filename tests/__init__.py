import pytest
import json
import logging

from blueprints import app

from flask import Flask, request

from app import cache, logging

from blueprints import db

import hashlib, uuid

from blueprints.user.model import Users
from blueprints.conversation.model import Conversations
from blueprints.group_message.model import MessageGroup
from blueprints.list_group.model import ListGroup
from blueprints.member_group.model import MemberGroup
from blueprints.personal_messages.model import PersonalMessages
from blueprints.status.model import StatusWA

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
    
    user_internal1 = Users(username='andre', phone_number='085735950340',password=hash_pass,salt= salt,status_internal= True)
    user_internal2 = Users(username='fajar', phone_number='085735950342',password=hash_pass,salt= salt,status_internal= True)
    user_noninternal = Users(username='andre', phone_number='085735950341',password=hash_pass,salt= salt,status_internal= False)
    conversation = Conversations(1, 2)
    message_group = MessageGroup(1, 1, 'halo')
    list_group = ListGroup('KITT')
    member_group = MemberGroup(1, 1)
    personal_message = PersonalMessages(1, 1, 'tes')
    status = StatusWA(1, 'status', 'gambar.jpg')
    db.session.add(user_internal1)
    db.session.add(user_internal2)
    db.session.add(user_noninternal)
    db.session.commit()
    db.session.add(list_group)
    db.session.commit()
    db.session.add(member_group)
    db.session.commit()
    db.session.add(message_group)
    db.session.commit()
    db.session.add(conversation)
    db.session.commit()
    db.session.add(personal_message)
    db.session.commit()
    db.session.add(status)
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
