import pypact
import json
from webtest import TestApp

TEST_POST = """{
            "description":"post request for user with id {24}",
            "provider_state":"There is a new user wih id {24}",
            "request":{
                "body":{
                    "firstName":"John",
                    "lastName":"Doe"
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "method":"post",
                "path":"/user",
                "query":"id=24"
            },
            "response":{
                "body":{
                    "result":true
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "status":201
            }
        }"""

TEST_POST_DIF_QUERY = """{
            "description":"post request for user with id {25}",
            "provider_state":"There is a new user wih id {25}",
            "request":{
                "body":{
                    "firstName":"John",
                    "lastName":"Doe"
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "method":"post",
                "path":"/user",
                "query":"id=25"
            },
            "response":{
                "body":{
                    "result":true
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "status":201
            }
        }"""

TEST_POST_DIF_BODY = """{
            "description":"post request for user with id {24}",
            "provider_state":"There is a new user wih id {24}",
            "request":{
                "body":{
                    "firstName":"John",
                    "lastName":"Deer"
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "method":"post",
                "path":"/user",
                "query":"id=24"
            },
            "response":{
                "body":{
                    "result":true
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "status":201
            }
        }"""

TEST_NO_BODY_NO_QUERY = """{
            "description":"get request for user",
            "provider_state":"There is a user",
            "request":{
                "method":"get",
                "path":"/user"
            },
            "response":{
                "body":{
                    "firstName":"John"
                },
                "headers":{
                    "Content-Type":"application/json"
                },
                "status":200
            }
        }"""

TEST_BODY_NOT_JSON_NO_RESPONSE = """{
            "description":"get request for alligator",
            "provider_state":"There is a alligator",
            "request":{
                "method":"post",
                "path":"/alligator",
                "body": "I am not json"
            },
            "response":{}
        }"""


def test_pypact_interaction():
    server = pypact.MockServer(host="localhost", port=1234)
    app = TestApp(server._app)

    test_post = json.dumps(json.loads(TEST_POST))
    assert app.post('/interactions', test_post).body == "Processed Interactions"

    test_post_body = """{
                         "firstName":"John",
                         "lastName":"Doe"
                     }"""
    assert app.post('/user?id=24', test_post_body).body == '{"result": true}'

    test_post_duplicate = json.dumps(json.loads(TEST_POST))
    assert app.post('/interactions', test_post_duplicate).body == "Processed Interactions"

    test_post_dif_query = json.dumps(json.loads(TEST_POST_DIF_QUERY))
    assert app.post('/interactions', test_post_dif_query).body == "Processed Interactions"

    test_post_body_dif_query = """{
                         "firstName":"John",
                         "lastName":"Doe"
                     }"""
    assert app.post('/user?id=25', test_post_body_dif_query).body == '{"result": true}'

    test_post_dif_body = json.dumps(json.loads(TEST_POST_DIF_BODY))
    assert app.post('/interactions', test_post_dif_body).body == "Processed Interactions"

    test_post_body_dif_body = """{
                         "firstName":"John",
                         "lastName":"Deer"
                     }"""
    assert app.post('/user?id=24', test_post_body_dif_body).body == '{"result": true}'

    test_no_body_no_query = json.dumps(json.loads(TEST_NO_BODY_NO_QUERY))
    assert app.post('/interactions', test_no_body_no_query).body == "Processed Interactions"

    assert app.get('/user').body == '{"firstName": "John"}'

    test_body_not_json_no_response = json.dumps(json.loads(TEST_BODY_NOT_JSON_NO_RESPONSE))
    assert app.post('/interactions', test_body_not_json_no_response).body == "Processed Interactions"

    assert app.post('/alligator', "I am not json").body == ''

    verification_body = app.get('/interactions/verification').body

    assert "Actual interactions do not match expected interactions." in verification_body

    test_post_body = """{
                         "firstName":"John",
                         "lastName":"Doe"
                     }"""
    assert app.post('/user?id=24', test_post_body).body == '{"result": true}'

    assert app.get('/interactions/verification').body == "Iteractions matched."

    assert app.delete('/interactions').body == "Cleared Interactions"

    try:
        app.post('/user?id=24', test_post_body)
    except Exception as e:
        assert "500" in str(e)
