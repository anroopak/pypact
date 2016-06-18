def safe_assign(dictionary, key_values):
    dictionary.update({key: value for key, value in key_values.iteritems() if value})
    return dictionary
