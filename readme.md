# Goldfinder

A Python CLI app to find materials in the Brandeis Goldfarb and Farber
libraries.

## Output

    $ goldfinder 'soviet art'
    Kunst und Revolution : Russische und Sowjetische Kunst 1910-1932 = Art and revolution : Russian and Soviet art 1910-1932 (c1988, Katalin Bakos; Österreichisches Museum für Angewandte Kunst; Mücsarnok (Budapest, Hungary))
    Farber 4, 22b: N6988 .K82 1988
    
    $ goldfinder 'soviet art' -a 2
    1. Kunst und Revolution : Russische und Sowjetische Kunst 1910-1932 = Art and
       revolution : Russian and Soviet art 1910-1932 (c1988, Katalin Bakos;
       Österreichisches Museum für Angewandte Kunst; Mücsarnok (Budapest,
       Hungary))
       Farber 4, 22b: N6988 .K82 1988
    2. Healthy spirit in a healthy body : representations of the sports body in
       Soviet art of the 1920s and 1930s (c2004, Levent, Nina Sobol 1971-)
       Farber 4, 24a: N8250 .L48 2004
    
    $ goldfinder 'NK3634.A2 C4566 1999' 'QA567.2.E44 K53 1992' 'PJ7745.I155 F313 1978'
    1. Character & context in Chinese calligraphy (c1999, Cary Y Liu (Cary Yee-
       Wei), 1955-; Dora C. Y Ching; Judith G. Smith 1941-; Princeton University.
       Art Museum)
       Farber 4, 36b: NK3634.A2 C4566 1999
    2. Elliptic curves (1992, Knapp, Anthony W)
       Goldfarb 2, 52b: QA567.2.E44 K53 1992
    3. The book of the superiority of dogs over many of those who wear clothes
       (c1978, Ibn al-Marzubān, Muḥammad ibn Khalaf d. 921 or 2. ; G. R Smith;
       Muḥammad ʻAbd al-Ḥalīm)
       Goldfarb M, 18b: PJ7745.I155 F313 1978
    
    $ goldfinder 'jellyfish' 'toads' 'birds' --amount 3 --separators --continue-numbering
    
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
    7. Birds, (1950, Menaboni, Athos 1895- ; Sara (Arnold) Menaboni)
       Goldfarb 2, 3a: + QL681 .M49
    8. Birds (c1990, Anderson, Walter Inglis 1903-1965 ; Mary Anderson Pickard)
       Farber 4, 21a: N6537.A48 A4 1990
    9. The Birds (1998, Paglia, Camille 1947-)
       Goldfarb 2, 13a: PN1997.B547 P35 1998
