import json

import requests


CLIENT_HEADERS = {
    'X-Pact-Mock-Service': 'true',
    'Content-Type': 'application/json'
}


class MockServerClient(requests.Session):

    def __init__(self, base_uri, *args, **kwargs):
        super(MockServerClient, self).__init__(*args, **kwargs)

        self.base_uri = base_uri
        self.headers.update(CLIENT_HEADERS)


    def get_verification(self):
        return self.get(
            '{}/interactions/verification'.format(self.base_uri)
            ).text


    def put_interactions(self, interaction):
        self.put(
            '{}/interactions'.format(self.base_uri),
            data=json.dumps(interaction)
        )


    def delete_interactions(self):
        result = self.delete('{}/interactions'.format(self.base_uri))
        return result.text


    def post_interactions(self, interaction):
        result = self.post(
            '{}/interactions'.format(self.base_uri),
            data=json.dumps(interaction)
        )
        return result.text


    def post_pact(self, pact_details):
        self.post(
            '{}/pact'.format(self.base_uri),
            data=json.dumps(pact_details)
        )
