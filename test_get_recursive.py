from _pytest.python_api import raises
from pytest import mark

from main import get_recursive, WrongJsonPathException, optional_chain


@mark.parametrize('args, my_json, default, expected', [
    [['primeiro'], {'primeiro': 'nao_default'}, 'default', 'nao_default'],
    [['primeiro'], {'nao_primeiro': 'nao default'}, 'default', 'default'],
])
def test_get_recursive_simple_case(args, my_json, default, expected):
    result = get_recursive(*args, my_json=my_json, default=default)

    assert result == expected


@mark.parametrize('args, my_json, default, expected', [
    [['primeiro', 'segundo'],
     {'primeiro': {'segundo': 'nao_default'}},
     'default',
     'nao_default'],
    [['primeiro', 'terceiro'],
     {'primeiro': {'segundo': 'nao_default'}},
     'default',
     'default'],
])
def test_get_recursive_two_depth(args, my_json, default, expected):
    result = get_recursive(*args, my_json=my_json, default=default)

    assert result == expected


@mark.parametrize(
    'args, my_json, default, expected_last_key, expected_last_value', [
        [['primeiro', 'segundo'],
         {'primeiro': ['segundo', 'nao_default']},
         'default',
         'primeiro',
         ['segundo', 'nao_default']],
        [['primeiro', 'segundo'],
         {'primeiro': {'segundo', 'nao_default'}},
         'default',
         'primeiro',
         {'segundo', 'nao_default'}],
        [['primeiro', 'segundo'],
         {'primeiro': 'segundo'},
         'default',
         'primeiro',
         'segundo'],
    ])
def test_get_recursive_wrong_key(args, my_json, default, expected_last_key,
                                 expected_last_value):
    with raises(WrongJsonPathException) as exec_info:
        get_recursive(*args, my_json=my_json, default=default)

    assert str(exec_info.value) == f'wrong path. last key used=' \
                                   f'{expected_last_key} with ' \
                                   f'value={str(expected_last_value)}'


@mark.parametrize('args, my_json, default, expected', [
    ['primeiro', {'primeiro': 'nao_default'}, 'default', 'nao_default'],
    ['primeiro', {'nao_primeiro': 'nao default'}, 'default', 'default'],
])
def test_optional_chain_simple_case(args, my_json, default, expected):
    result = optional_chain(my_json, args, default)

    assert result == expected


@mark.parametrize('args, my_json, default, expected', [
    ['primeiro.segundo',
     {'primeiro': {'segundo': 'nao_default'}},
     'default',
     'nao_default'],
    ['primeiro.terceiro',
     {'primeiro': {'segundo': 'nao_default'}},
     'default',
     'default'],
])
def test_optional_chain_two_depth(args, my_json, default, expected):
    result = optional_chain(my_json, args, default)

    assert result == expected


@mark.parametrize(
    'args, my_json, default, expected_last_key, expected_last_value', [
        ['primeiro.segundo',
         {'primeiro': ['segundo', 'nao_default']},
         'default',
         'primeiro',
         None],
        ['primeiro.segundo',
         {'primeiro': {'segundo', 'nao_default'}},
         'default',
         'primeiro',
         None],
        ['primeiro.segundo',
         {'primeiro': 'segundo'},
         'default',
         'primeiro',
         None],
    ])
def test_optional_chain_wrong_key(args, my_json, default, expected_last_key,
                                  expected_last_value):
    result = optional_chain(my_json, args, default)

    assert result is None
