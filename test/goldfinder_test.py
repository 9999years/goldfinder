import goldfinder

import test_constants

def search(term, max_count=10, extra_params={}):
    global results
    ret = results[term]
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
        == 'Marx (c2004, Collier, Andrew 1944-)\n'
        'Goldfarb M, 3a: B3305.M74 C56 2004')

def test_integration_local():
    assert (
'''1. Jellyfish (2008, Yael Fogiel; Laetitia Gonzalez; Amir Harel; Ayelet Kait;
   Shirah Gefen; Etgar Keret 1967-; Sarah Adler; Nikol Leidman; Gera Sandler;
   Noa Knoller; Ma-Nenita de Latorre; Zharira Charifai; Meduzot Limited
   Partnership (Firm); Films du Poisson (Firm); Lama Productions Ltd.; Israeli
   Film Fund (Firm); Arte France cinéma (Firm); Studio Canal+.; Zeitgeist
   Films.)
   Goldfarb 1, DVD Collection 2: PN1997 .J41 2008
2. Gimme green (c2006, Isaac Brown (Isaac Oviatt); Eric Flagg; University of
   Florida. Documentary Institute.; Jellyfish Smack Productions.)
   Goldfarb 1, DVD Collection 2: SB433 .G56 2006
3. Starfish, jellyfish, and the order of life : issues in nineteenth-century
   science (c1976, Winsor, Mary P)
   Goldfarb 2, 55b: QL362.5 .W56'''
    == goldfinder.get_directions(['jellyfish'], amount=3))

    assert (
'''
        JELLYFISH
        ---------
1. Jellyfish (2008, Yael Fogiel; Laetitia Gonzalez; Amir Harel; Ayelet Kait;
   Shirah Gefen; Etgar Keret 1967-; Sarah Adler; Nikol Leidman; Gera Sandler;
   Noa Knoller; Ma-Nenita de Latorre; Zharira Charifai; Meduzot Limited
   Partnership (Firm); Films du Poisson (Firm); Lama Productions Ltd.; Israeli
   Film Fund (Firm); Arte France cinéma (Firm); Studio Canal+.; Zeitgeist
   Films.)
   Goldfarb 1, DVD Collection 2: PN1997 .J41 2008
2. Gimme green (c2006, Isaac Brown (Isaac Oviatt); Eric Flagg; University of
   Florida. Documentary Institute.; Jellyfish Smack Productions.)
   Goldfarb 1, DVD Collection 2: SB433 .G56 2006
3. Starfish, jellyfish, and the order of life : issues in nineteenth-century
   science (c1976, Winsor, Mary P)
   Goldfarb 2, 55b: QL362.5 .W56

        TOADS
        -----
4. The frog book; North American toads and frogs, with a study of the habits
   and life histories of those of the northeastern States. (1969, Dickerson,
   Mary Cynthia 1866-1923.)
   Goldfarb 2, 55b: QL651 .D54 1969
5. Handbook of frogs and toads of the United States and Canada, (1949, Wright,
   Anna (Allen) 1882- ; Albert Hazen Wright 1879-)
   Goldfarb 2, 55b: QL668.E2 W8 1949
6. Toads of war (1979, Iroh, Eddie)
   Goldfarb 2, 38a: PR9387.9.I7 T6

        BIRDS
        -----
7. Birds,  (1950, Menaboni, Athos 1895- ; Sara (Arnold) Menaboni)
   Goldfarb 2, 3a: + QL681 .M49
8. Birds (c1990, Anderson, Walter Inglis 1903-1965 ; Mary Anderson Pickard)
   Farber 4, 21a: N6537.A48 A4 1990
9. The Birds (1998, Paglia, Camille 1947-)
   Goldfarb 2, 13a: PN1997.B547 P35 1998'''
    == goldfinder.get_directions(['jellyfish', 'toads', 'birds'],
        amount=3, separators=True, continue_numbering=True))

def test_bib():
    goldfinder.sys.stdin.readlines = lambda: bibtex
