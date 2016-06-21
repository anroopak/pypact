class Matcher(object):
    """
    The matcher class provides methods which allow terms to be matched on. By
    doing so, it allows more flexible tests not bound to a particular value.

    After implementing each method, a user might want to use the `dumps`
    function in the stdlib `json` package.
    """

    @classmethod
    def eachLike(cls, contents, minimumRequired):
        return {
            'json_class': 'Pact::ArrayLike',
            'contents': contents,
            'min': minimumRequired
        }

    @classmethod
    def like(cls, contents):
        return {
            'json_class': 'Pact::SomethingLike',
            'contents': contents
        }

    @classmethod
    def term(cls, generate, matcher):
        return {
            'json_class': 'Pact::Term',
            'data': {
                'generate': generate,
                'matcher': {
                    'json_class': 'Regexp',
                    'o': 0,
                    's': matcher
                }
            }
        }
