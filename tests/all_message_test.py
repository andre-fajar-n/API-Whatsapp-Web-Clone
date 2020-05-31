import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestAllMessage():
    def test_get_all_message(self, client, init_database):
        token = create_token_internal()
        res = client.get('/all_message', 
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json' )
        
        res_json = json.loads(res.data)
        assert res.status_code == 200