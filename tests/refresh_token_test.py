import json, logging
from . import app, client, cache, create_token_internal, create_token_noninternal, init_database

class TestRefreshToken():
    def test_refresh_token(self, client, init_database):
        token = create_token_internal()
        res = client.post('/login/refresh',
                         content_type='application/json',
                         headers={'Authorization':'Bearer ' + token},)
        
        assert res.status_code == 200