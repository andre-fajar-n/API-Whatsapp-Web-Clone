import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestGroupMessage():
    def test_post_valid_group(self, client, init_database):
        data = {
            'group_chat_id':1,
            'message': 'tes'
        }
        token = create_token_internal()
        res = client.post('/message_group',
                          headers={'Authorization':'Bearer ' + token},
                          content_type='application/json',
                          query_string=data)
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_post_invalid_group(self, client, init_database):
        data = {
            'group_chat_id':10,
            'message': 'tes'
        }
        token = create_token_internal()
        res = client.post('/message_group',
                          headers={'Authorization':'Bearer ' + token},
                          content_type='application/json',
                          query_string=data)
        
        res_json = json.loads(res.data)
        assert res.status_code == 404