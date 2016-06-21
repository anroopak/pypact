from __future__ import absolute_import


class Interaction(object):
    """
    Builder for interaction dictionaries. Most of the methods in this class
    return the instance back. This is to be able to chain them. An instance ends
    up looking something like:
        {
        }
    """

    def __init__(self, add_method):
        self.add_method = add_method

        self.provider_state = None
        self.description = None
        self.request = None
        self.response = None

    def __str__(self):
        return '{}-{}'.format(self.provider_state, self.description)

    def to_json(self):
        return {
            'provider_state': self.provider_state,
            'description': self.description,
            'request': self.request,
            'response': self.response
        }

    def given(self, provider_state):
        self.provider_state = provider_state
        return self

    def upon_receiving(self, description):
        self.description = description
        return self

    def with_request(self, method, path, query=None, headers=None, body=None):
        self.request = {
            'method': method.lower(),
            'path': path,
            'query': query,
            'headers': headers,
            'body': body
        }

        return self

    def will_respond_with(self, status, headers=None, body=None):
        self.response = {
            'status': status,
            'headers': headers,
            'body': body
        }

        self.add_interaction()

        return self

    def add_interaction(self):
        self.add_method({
            'provider_state': self.provider_state,
            'description': self.description,
            'request': self.request,
            'response': self.response
        })
