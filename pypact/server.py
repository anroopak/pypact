import json
import StringIO
import logging

from bottle import template, request, response, HTTPResponse, Bottle
from datetime import datetime
from pypact.verifications import VerificationResults

class MockServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.dynamic_routes = []
        self.registered_interactions = {}
        self.received_requests = {}
        self._app = Bottle()
        self._route()


    def _route(self):
        self._app.route(path='/interactions', method=['POST', 'DELETE'], callback=self._interactions)
        self._app.route(path='/interactions/verification', method='GET', callback=self._verification)


    def start(self):
        self._app.run(host=self._host, port=self._port)


    def dynamic_route(self):
        if request.query_string != '':
            query = request.query_string
        else:
            query = 'no_query_string'

        if request.body.getvalue() != '':
            body = request.body.getvalue()
            try:
                body = json.loads(body)
            except (TypeError, Exception) as e:
                logging.warning('The body in this request is not json: %s' % (e))
        else:
            body = 'no_body'

        for dr in self.dynamic_routes:
            if dr['method'] != request.method:
                continue
            if dr['path'] != request.path:
                continue
            if dr['query'] != query:
                continue
            if dr['body'] != body:
                continue
            r = dr['response']
            dr['received_requests'] = dr['received_requests'] + 1
            break

        string_headers = {}
        for i, v in r['headers'].iteritems():
          string_headers[str(i)] = str(v)


        return HTTPResponse(status=r['status'], body=r['body'], headers=string_headers)


    def clear_route(self):
        return HTTPResponse(status=500)


    def append_route(self, description, provider_state, method, path, query, body, pact_response):
        self.dynamic_routes.append(
            {
                'description': description,
                'provider_state': provider_state,
                'method': method,
                'path': path,
                'query': query,
                'body': body,
                'response': pact_response,
                'received_requests': 0,
                'expected_requests': 1
            }
        )


    def _interactions(self):
        if request.method == 'POST':

            interaction = json.loads(request.body.read())

            pact_request = interaction['request']
            pact_response = interaction['response']

            path = pact_request['path']
            method = pact_request['method'].upper()
            description = interaction['description']
            provider_state = interaction['provider_state']
            if 'query' in pact_request:
                query = pact_request['query']
            else:
                query = 'no_query_string'
            if 'body' in pact_request:
                body = pact_request['body']
            else:
                body = 'no_body'



            if 'headers' not in pact_response:
                pact_response['headers'] = {}

            if 'status' not in pact_response:
                pact_response['status'] = 200

            if 'body' not in pact_response:
                pact_response['body'] = ''

            if len(self.dynamic_routes) == 0:
                self.append_route(description, provider_state, method, path, query, body, pact_response)
            else:
                match = False
                for dr in self.dynamic_routes:
                    if (dr['description'] == description and dr['provider_state'] == provider_state and dr['method'] == method 
                        and dr['path'] == path and dr['query'] == query and dr['body'] == body and dr['response'] == pact_response):
                        dr['expected_requests'] = dr['expected_requests'] + 1
                        match = True
                        break
                if match == False:
                    self.append_route(description, provider_state, method, path, query, body, pact_response)
            methods = []
            for dr in self.dynamic_routes:
                if dr['path'] == path:
                    methods.append(dr['method'])

            self._app.route(path, methods, self.dynamic_route)

            self.registered_interactions.update(interaction)

            return 'Processed Interactions'

        elif request.method == 'DELETE':

            routes_to_clear = []
            for _route in self._app.routes:
                if _route.rule != '/interactions':
                    routes_to_clear.append(_route)        
            for _route in routes_to_clear:
                self._app.route(_route.rule, _route.method, self.clear_route)
            self.registered_interactions = {}
            return 'Cleared Interactions'


    def _verification(self):
        mismatched = True
        vr = VerificationResults()
        mismatched_interactions = []
        
        for dr in self.dynamic_routes:
            if dr['expected_requests'] != dr['received_requests']:
                mismatched = False
                mismatched_interactions.append(dr)

        if mismatched == True:
            return vr.VerificationPassed()
        else:
            return vr.VerificationFailed() % (mismatched_interactions)
