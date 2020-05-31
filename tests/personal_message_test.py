import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestPersonalMessage():
    def test_post(self, client, init_database):
        data = {
            'user2_id': 1,
            'message': 'tes'
        }
        token = create_token_internal()
        res = client.post('/personal_message',
                          query_string=data,
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_delete_valid_id(self, client, init_database):
        token = create_token_internal()
        res = client.delete('/personal_message/1',
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_delete_invalid_id(self, client, init_database):
        token = create_token_internal()
        res = client.delete('/personal_message/10',
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404