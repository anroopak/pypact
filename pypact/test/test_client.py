import json
import pypact
import pytest
import requests
import requests_mock


TEST_BASE_URI = 'mock://127.0.0.1:1234'

@pytest.fixture
def client():
    return pypact.MockServerClient(TEST_BASE_URI)


@pytest.fixture
def mock_request(client):
    adapter = requests_mock.Adapter()
    client.mount('mock', adapter)
    return adapter


def test_client_creation(client):
    assert client.base_uri == TEST_BASE_URI

    for header in client.headers.items():
        assert header in client.headers.items()


def test_client_get_verification(client, mock_request):
    mock_request.register_uri(
        'GET',
        '{}/interactions/verification'.format(TEST_BASE_URI),
        text='')

    verification = client.get_verification()

    assert verification == ''
    assert mock_request.call_count == 1


def test_client_put_interaction(client, mock_request):
    mock_request.register_uri(
        'PUT',
        '{}/interactions'.format(TEST_BASE_URI))

    client.put_interactions([{}])

    assert mock_request.call_count == 1
    assert mock_request.request_history[0].json() == [{}]


def test_client_delete_interaction(client, mock_request):
    mock_request.register_uri(
        'DELETE',
        '{}/interactions'.format(TEST_BASE_URI))

    client.delete_interactions()

    assert mock_request.call_count == 1


def test_client_post_interaction(client, mock_request):
    mock_request.register_uri('POST', '{}/interactions'.format(TEST_BASE_URI))

    client.post_interactions({})

    assert mock_request.call_count == 1
    assert mock_request.request_history[0].json() == {}


def test_client_post_pact(client, mock_request):
    mock_request.register_uri('POST', '{}/pact'.format(TEST_BASE_URI))

    client.post_pact({})

    assert mock_request.call_count == 1
    assert mock_request.request_history[0].json() == {}

