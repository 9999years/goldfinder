import goldfinder

import test_constants

def search(term, max_count=10, extra_params={}):
    ret = test_constants.results[term]
    if len(ret) > max_count:
        return ret[:max_count]
    else:
        return ret

# hoooo my god this cant be good
goldfinder.search = search
goldfinder.get_directions.__globals__['search'] = search

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
    assert (goldfinder.pretty(search('marx')[0])
        == 'Marx (Collier, Andrew 1944-, c2004)\n'
        'Goldfarb M, 3a: B3305.M74 C56 2004')

def test_integration_local():
    assert (
'''1. Jellyfish (Yael Fogiel; Laetitia Gonzalez; Amir Harel; Ayelet Kait; Shirah
   Gefen; Etgar Keret 1967-; Sarah Adler; Nikol Leidman; Gera Sandler; Noa
   Knoller; Ma-Nenita de Latorre; Zharira Charifai; Meduzot Limited
   Partnership (Firm); Films du Poisson (Firm); Lama Productions Ltd.; Israeli
   Film Fund (Firm); Arte France cinéma (Firm); Studio Canal+.; Zeitgeist
   Films., 2008)
   Goldfarb 1, DVD Collection 2: PN1997 .J41 2008
2. Gimme green (Isaac Brown (Isaac Oviatt); Eric Flagg; University of Florida.
   Documentary Institute.; Jellyfish Smack Productions., c2006)
   Goldfarb 1, DVD Collection 2: SB433 .G56 2006
3. Starfish, jellyfish, and the order of life : issues in nineteenth-century
   science (Winsor, Mary P, c1976)
   Goldfarb 2, 55b: QL362.5 .W56'''
    == goldfinder.get_directions(['jellyfish'], amount=3))

    assert (
'''
        JELLYFISH
        ---------
1. Jellyfish (Yael Fogiel; Laetitia Gonzalez; Amir Harel; Ayelet Kait; Shirah
   Gefen; Etgar Keret 1967-; Sarah Adler; Nikol Leidman; Gera Sandler; Noa
   Knoller; Ma-Nenita de Latorre; Zharira Charifai; Meduzot Limited
   Partnership (Firm); Films du Poisson (Firm); Lama Productions Ltd.; Israeli
   Film Fund (Firm); Arte France cinéma (Firm); Studio Canal+.; Zeitgeist
   Films., 2008)
   Goldfarb 1, DVD Collection 2: PN1997 .J41 2008
2. Gimme green (Isaac Brown (Isaac Oviatt); Eric Flagg; University of Florida.
   Documentary Institute.; Jellyfish Smack Productions., c2006)
   Goldfarb 1, DVD Collection 2: SB433 .G56 2006
3. Starfish, jellyfish, and the order of life : issues in nineteenth-century
   science (Winsor, Mary P, c1976)
   Goldfarb 2, 55b: QL362.5 .W56

        TOADS
        -----
4. The frog book; North American toads and frogs, with a study of the habits
   and life histories of those of the northeastern States. (Dickerson, Mary
   Cynthia 1866-1923., 1969)
   Goldfarb 2, 55b: QL651 .D54 1969
5. Handbook of frogs and toads of the United States and Canada, (Wright, Anna
   (Allen) 1882- ; Albert Hazen Wright 1879-, 1949)
   Goldfarb 2, 55b: QL668.E2 W8 1949
6. Toads of war (Iroh, Eddie, 1979)
   Goldfarb 2, 38a: PR9387.9.I7 T6

        BIRDS
        -----
7. Birds,  (Menaboni, Athos 1895- ; Sara (Arnold) Menaboni, 1950)
   Goldfarb 2, 3a: + QL681 .M49
8. Birds (Anderson, Walter Inglis 1903-1965 ; Mary Anderson Pickard, c1990)
   Farber 4, 21a: N6537.A48 A4 1990
9. The Birds (Paglia, Camille 1947-, 1998)
   Goldfarb 2, 13a: PN1997.B547 P35 1998'''
    == goldfinder.get_directions(['jellyfish', 'toads', 'birds'],
        amount=3, separators=True, continue_numbering=True))

def test_bib():
    goldfinder.sys.stdin.readlines = lambda: test_constants.bibtex
