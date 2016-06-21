from __future__ import absolute_import

from pypact.matcher import Matcher


def test_like():
    contents = {
        'json_class': 'Pact::SomethingLike',
        'contents': 23
    }
    expected_contents = Matcher.like(23)
    assert contents == expected_contents

    contents = {
        'json_class': 'Pact::SomethingLike',
        'contents': 'Copacetic'
    }
    expected_contents = Matcher.like('Copacetic')
    assert contents == expected_contents

    contents = {
        'json_class': 'Pact::SomethingLike',
        'contents': [1, 2]
    }
    expected_contents = Matcher.like([1, 2])
    assert contents == expected_contents

    contents = {
        'json_class': 'Pact::SomethingLike',
        'contents': {'doctor_name': 'Harrison Wells'}
    }
    expected_contents = Matcher.like({'doctor_name': 'Harrison Wells'})
    assert contents == expected_contents


def test_each_like():
    contents = {
        'json_class': 'Pact::ArrayLike',
        'contents': [4, 5],
        'min': 2
    }
    expected_contents = Matcher.eachLike([4, 5], 2)
    assert contents == expected_contents

    contents = {
        'json_class': 'Pact::ArrayLike',
        'contents': 13,
        'min': 1
    }

    expected_contents = Matcher.eachLike(13, 1)
    assert expected_contents == contents

    contents = {
        'json_class': 'Pact::ArrayLike',
        'contents': 'zoom',
        'min': 8
    }

    expected_contents = Matcher.eachLike('zoom', 8)
    assert expected_contents == contents

    contents = {
        'json_class': 'Pact::ArrayLike',
        'contents': {'catch_phrase': 'hello children'},
        'min': 4
    }

    expected_contents = Matcher.eachLike({'catch_phrase': 'hello children'}, 4)

    assert expected_contents == contents

    contents = {
        'json_class': 'Pact::ArrayLike',
        'contents': {'favorite_foods': {
            'json_class': 'Pact::ArrayLike',
            'contents': ['cocoa puffs', 'peanut butter'],
            'min': 5
        }},
        'min': 1
    }

    expected_contents = Matcher.eachLike({
        'favorite_foods': Matcher.eachLike(['cocoa puffs', 'peanut butter'], 5)
    }, 1)

    assert expected_contents == contents


def test_term():
    term = {
        'json_class': 'Pact::Term',
        'data': {
            'generate': 'juxtapose',
            'matcher': {'json_class': 'Regexp', 'o': 0, 's': '\\w'}
        }
    }

    expected_term = Matcher.term('juxtapose', '\\w')
    assert term == expected_term

    term = {
        'json_class': 'Pact::Term',
        'data': {
            'generate': 'yes',
            'matcher': {'json_class': 'Regexp', 'o': 0, 's': 'yes|no|maybe'}
        }
    }

    expected_term = Matcher.term('yes', 'yes|no|maybe')
    assert term == expected_term
