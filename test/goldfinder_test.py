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
        'maps': [{
            'mapurl': 'https://brandeis.stackmap.com/map/?floor=5&r=458',
            'library': 'Brandeis University Library',
            'height': 717,
            'ranges': [{
                'startcallno': 'B2799. K7.S25 1994',
                'rangeno': 458,
                'callnos': [{
                    'start': 'B2799. K7.S25 1994',
                    'end': 'BD161. R48 1987'}],
                'rangename': '3a',
                'coordinates': [[872.5, 620.5],
                    [876.5, 620.5],
                    [876.5, 380.5],
                    [872.5, 380.5]],
                'label': '3a',
                'callnoDisplay': 'B2799. K7.S25 1994 <--> BD161. R48 1987',
                'endcallno': 'BD161. R48 1987',
                'y': 500.5,
                'x': 874.5}],
            'width': 1250,
            'directions': 'Please proceed to the mezzanine level of the Goldfarb building of the Brandeis University Library.',
            'floorname': 'Farber Mezzanine / Goldfarb Mezzanine'},
            {'mapurl': 'https://brandeis.stackmap.com/map/?floor=3&r=233',
            'library': 'Brandeis University Library',
            'height': 717,
            'ranges': [{
                'startcallno': 'AS911. N72 1934',
                'rangeno': 233,
                'callnos': [{
                    'start': 'AS911. N72 1934',
                    'end': 'CB361. B5 V.18'}],
                'rangename': '4a',
                'coordinates': [[664.5, 407.5],
                    [668.5, 407.5],
                    [668.5, 259.5],
                    [664.5, 259.5]],
                    'label': '4a',
                    'callnoDisplay': 'AS911. N72 1934 <--> CB361. B5 V.18',
                    'endcallno': 'CB361. B5 V.18',
                    'y': 333.5,
                    'x': 666.5}],
            'width': 1250,
            'directions': 'Please proceed to the third floor of Brandeis University Library.  Stacks are located in Farber (Ms) and Goldfarb (A, C-G including oversized (+) as well as the double oversized collection (++) excluding ++ Ns.',
            'floorname': 'Farber 3 / Goldfarb 3'}],
        'callno': 'B3305.M74 C56 2004',
        'location': 'Stacks',
        'library': 'Main Library',
        'aisle': '3a',
        'floor': 'M',
        'building': 'Goldfarb'
    }
}

def test_pretty():
    assert (goldfinder.pretty(complete)
        == 'Marx (c2004, Collier, Andrew 1944-)\n'
        'Goldfarb M, 3a: B3305.M74 C56 2004')
