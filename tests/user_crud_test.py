import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestUserCrud():
    def test_post_user(self, client, init_database):
        data = {
            'phone_number':'085555555555',
            'password':'password'
        }
        res = client.post('/user', 
                          data=json.dumps(data),
                          content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_user(self, client, init_database):
        token = create_token_internal()
        res = client.get('/user', 
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json' )
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_patch_user(self, client, init_database):
        token = create_token_internal()
        data = {
            'phone_number':'081111111111',
            'password':'new'
        }
        res = client.patch('/user',
                           headers={'Authorization':'Bearer ' + token},
                           content_type='application/json',
                           data=json.dumps(data))
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_delete_id_valid_admin(self, client, init_database):
        res = client.delete('/user/admin/1',
                            content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_delete_id_invalid_admin(self, client, init_database):
        res = client.delete('/user/admin/10',
                            content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_get_admin_asc(self, client, init_database):
        data = {
            'orderby':'phone_number',
        }
        res = client.get('/user/admin',
                         query_string=data,
                         content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_admin_desc(self, client, init_database):
        data = {
            'orderby':'phone_number',
            'sort':'desc'
        }
        res = client.get('/user/admin',
                         query_string=data,
                         content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200