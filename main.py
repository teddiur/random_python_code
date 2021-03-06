from functools import reduce


class WrongJsonPathException(BaseException):
    pass


def get_recursive(*args, my_json=None, default=None):
    head = args[0]
    tail = args[1:]
    inner = my_json.get(head, default)

    if len(tail) == 0:
        return inner

    elif inner is None:
        return inner

    elif type(inner) != dict:
        raise WrongJsonPathException(f'wrong path. last key used='
                                     f'{head} with value={str(inner)}')
    else:
        return get_recursive(*tail, my_json=inner, default=default)


def optional_chain(root, keys, default):
    try:
        return reduce(lambda my_dict, key: my_dict.get(key, default),
                      keys.split('.'),
                      root)
    except AttributeError:
        return None
