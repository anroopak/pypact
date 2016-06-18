import pypact
import requests
import time

from multiprocessing import Process


def start_server(server):
    server.start()


def register_interaction(url, action, interaction=None):
    client = pypact.MockServerClient(url)
    if action == 'post':
        interaction = interaction.to_json()
        result = client.post_interactions(interaction)
    elif action == 'delete':
        result = client.delete_interactions()
    elif action == 'verify':
        result = client.get_verification()
    return result


def build_pact(builder, interactions):
    pact = builder.parse_participants()
    builder.persist_pact(pact, interactions)


def test_server(argv=None):
    consumer = 'My consumer'
    provider = 'My provider'
    port = '1234'
    path = './pacts'

    builder = pypact.Builder(consumer, provider, port, path)
    service = builder.service

    server = pypact.MockServer(host='localhost', port=8080)
    p = Process(target=start_server, args=(server,))
    p.daemon = True
    p.start()
    time.sleep(3)

    interaction = (
        service.given('There is a user with id {23}')
               .upon_receiving('get request for user with id {23}')
               .with_request(method='GET', path='/user', query='id=23')
               .will_respond_with(
                    status=200,
                    headers={'Content-Type': 'application/json'},
                    body={'firstName': 'John'}
            )
    )

    url = 'http://localhost:8080'
    action = 'post'

    result = register_interaction(url, action, interaction)

    name = requests.get('http://localhost:8080/user?id=23')
    print name.text

    body = {
            'firstName': 'John',
            'lastName': 'Doe'
    }
    headers = {
            'Content-Type': 'application/json'
    }

    interaction = (
        service.given('There is a new user wih id {24}')
               .upon_receiving('post request for user with id {24}')
               .with_request(method='POST', path='/user', query='id=24', body=body, headers=headers)
               .will_respond_with(
                    status=201,
                    headers={'Content-Type': 'application/json'},
                    body={'result': True}
               )
    )

    result = register_interaction(url, action, interaction)

    name = requests.post('http://localhost:8080/user?id=24', json=body)
    print name.text

    body = {
        'firstName': 'John',
        'lastName': 'Deer'
    }

    interaction = (
        service.given('There is a new user wih id {24}')
               .upon_receiving('post request for user with id {24}')
               .with_request(method='POST', path='/user', query='id=24', body=body, headers=headers)
               .will_respond_with(
                    status=201,
                    headers={'Content-Type': 'application/json'},
                    body={'result': False}
               )
    )

    result = register_interaction(url, action, interaction)

    name = requests.post('http://localhost:8080/user?id=24', json=body)
    print name.text

    interaction = (
        service.given('There is a new user wih id {24}')
               .upon_receiving('post request for user with id {24}')
               .with_request(method='PUT', path='/user', query='id=24', body=body, headers=headers)
               .will_respond_with(
                    status=200,
                    headers={'Content-Type': 'application/json'},
                    body={'text': 'Upload Successful'}
               )
    )

    result = register_interaction(url, action, interaction)
    result = register_interaction(url, action, interaction)

    name = requests.put('http://localhost:8080/user?id=24', json=body)
    print name.text

    action = 'verify'
    result = register_interaction(url, action)
    print result

    action = 'delete'
    result = register_interaction(url, action)

    p.terminate()

    build_pact(builder, service.interactions)
