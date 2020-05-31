import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestListGroup():
    def test_post(self, client, init_database):
        data = {
            'name': 'andre'
        }
        token = create_token_internal()
        res = client.post('/list_group',
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization':'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200