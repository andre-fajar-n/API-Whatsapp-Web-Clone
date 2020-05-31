import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestMemberGroup():
    def test_post_valid_group(self, client, init_database):
        data = {
            'group_chat_id': 1,
            'user_id': 2
        }
        token = create_token_internal()
        res = client.post('/member_group',
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_post_invalid_group(self, client, init_database):
        data = {
            'group_chat_id': 10,
            'user_id': 2
        }
        token = create_token_internal()
        res = client.post('/member_group',
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_get_valid_group(self, client, init_database):
        data = {
            'group_chat_id':1
        }
        token = create_token_internal()
        res = client.get('/member_group',
                         data=json.dumps(data),
                         headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_invalid_group(self, client, init_database):
        data = {
            'group_chat_id':10
        }
        token = create_token_internal()
        res = client.get('/member_group',
                         data=json.dumps(data),
                         headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404