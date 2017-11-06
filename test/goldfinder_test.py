import goldfinder

complete = {
    'library': 'Main Library',
    'collection': 'Stacks',
    'call': 'B3305.M74 C56 2004',
    'title': 'Marx',
    'author': 'Collier, Andrew 1944-',
    'details': '',
    'year': 'c2004',
    'directions': {
        'floor': 'M',
        'building': 'Goldfarb',
        'aisle': '3a',
        'english': 'Please proceed to the third floor of Brandeis University Library.  Stacks are located in Farber (Ms) and Goldfarb (A, C-G including oversized (+) as well as the double oversized collection (++) excluding ++ Ns.',
    },
}

def _test_building(expected, directions):
    mock = { 'maps': [{
                'directions': directions,
    }]}
    assert expected == goldfinder.get_building(mock)

def test_building():
    _test_building('Goldfarb', 'Please proceed to the mezzanine level of the '
        'Goldfarb building of the Brandeis University Library')
    _test_building('Goldfarb', 'Please proceed to the first floor of Goldfarb '
        'building of the Brandeis University Library')
    _test_building('Farber', 'Please proceed to the fourth floor of the Farber '
            'building of the Brandeis University Library.')
    _test_building('Goldfarb / Farber', '')

def test_pretty():
    assert (goldfinder.pretty(complete)
        == 'Marx (c2004, Collier, Andrew 1944-)\n'
        'Goldfarb M, 3a: B3305.M74 C56 2004')
