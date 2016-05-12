import pytest
import pypact
import os

CONSUMER_NAME = 'My Service Consumer'
PROVIDER_NAME = 'My Service Provider'
PORT = 1234
PATH = './pacts-test'


@pytest.fixture
def builder():
    return pypact.Builder(consumer=CONSUMER_NAME, provider=PROVIDER_NAME, port=PORT, path=PATH)


PACT = {'consumer': 'my service consumer', 'provider': 'my service provider'}


def test_parse_participants(builder):
    participants = builder.parse_participants()
    assert PACT == participants


INTERACTIONS = {}


def test_persist_pact(builder):
    builder.persist_pact(pact=PACT, interactions=INTERACTIONS)
    assert os.path.isfile('%s/my_service_consumer-my_service_provider.json' % (PATH))


@pytest.fixture
def null_consumer_builder():
    return pypact.Builder(consumer='', provider=PROVIDER_NAME, port=PORT, path=PATH)


def test_null_conumer_parse_participants(null_consumer_builder):
    with pytest.raises(pypact.PyPactException):
            null_consumer_builder.parse_participants()


@pytest.fixture
def null_provider_builder():
    return pypact.Builder(consumer=CONSUMER_NAME, provider='', port=PORT, path=PATH)


def test_null_provider_parse_participants(null_provider_builder):
    with pytest.raises(pypact.PyPactException):
            null_provider_builder.parse_participants()
