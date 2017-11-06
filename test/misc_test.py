from goldfinder import misc

def _test_get_in(expected, obj, *keys):
    assert expected == misc.get_in(obj, *keys)

def test_get_in():
    obj = {'a': 1, 'b': 2, 'c': {
        'foo': [1, 2],
        'bar': False,
        },
        'z': [2, 3, 4]
    }
    _test_get_in(1, obj, 'a')
    _test_get_in(False, obj, 'c', 'bar')
    _test_get_in(3, obj, 'z', 1)
