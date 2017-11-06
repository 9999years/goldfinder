import requests
import argparse
from urllib import parse as urlparse
from lxml import html
import re
import zs.bibtex

# local
from goldfinder import misc

def search_raw(search_term, extra_params={}):
    params = {
        'mode': 'Basic',
        'vid': 'BRAND',
        'vl(freeText0)': search_term,
        'fn': 'search',
        'tab': 'alma',
        'fctN': 'facet_tlevel',
        'fctV': 'available',
    }

    params.update(extra_params)

    url = 'http://search.library.brandeis.edu/primo_library/libweb/action/search.do'

    r = requests.get(url, params=params)
    status = misc.check_internet(r)
    if status is None:
        misc.err(status)
    return r

def get_english(directions):
    return misc.get_in(directions, 'maps', 0, 'directions')

def get_aisle(directions):
    return misc.get_in(directions, 'maps', 0, 'ranges', 0, 'label') or ''

def get_floor(directions):
    url = misc.get_in(directions, 'maps', 0, 'mapurl')
    if url is None:
        return ''
    url = urlparse.urlparse(url)
    params = urlparse.parse_qs(url.query)
    floor = misc.get_in(params, 'floor', 0)
    if floor is None:
        return ''
    else:
        if floor == '5':
            return 'M'
        else:
            return int(floor)

def get_building(directions):
    """
    gets the building from an item's directions
    """
    # something like: Please proceed to the mezzanine level of the Goldfarb
    default = 'Goldfarb / Farber'
    directions = misc.get_in(directions, 'maps', 0, 'directions')
    if directions is None:
        return default
    matches = re.search(r'(Goldfarb|Farber) building', directions)
    if matches is None:
        return default
    groups = matches.groups()
    if len(groups) == 0:
        return default
    else:
        return groups[0]

def get_raw_directions(item):
    if 'directions' in item:
        return item['directions']

    params = {
        'holding[]': '{library}$${collection}$${call}'.format(**item),
        'alt': 'true',
    }

    url = 'https://brandeis.stackmap.com/json/'

    r = requests.get(url, params=params)
    status = misc.check_internet(r)
    if status is None:
        misc.err(status)
        return

    try:
        directions = r.json()
    except json.decoder.JSONDecodeError as e:
        # ¯\_(ツ)_/¯
        return

    return misc.get_in(directions, 'results', 0)

def add_directions(item):
    directions = get_raw_directions(item)
    item['directions'] = {}
    item['directions']['building'] = get_building(directions)
    item['directions']['floor']    = get_floor(directions)
    item['directions']['aisle']    = get_aisle(directions)
    # item['directions']['english']  = get_english(directions)

def search(search_term, max_count=10, extra_params={}):
    """
    returns a list of item dicts with the following keys:
    library: usually Main Library
    collection: usually Stacks, sometimes Media or Microfiche
    call: call number, something like B3305.M74 C56 2004
    title: item title
    author: last, first, birth-death, something like 'Collier, Andrew 1944-' but
        can get really verbose
    details: unused (i think?)
    year: something like c2004
    directions: dict containing:
        building: Goldfarb or Farber (unless errors, in which case
            Goldfarb/Farber)
        floor: 1-4 (4 is farber only) or M (goldfarb only)
        aisle: something like 3a
        english: plain-english directions, something like "Please proceed to the
            third floor of Brandeis University Library." but strangely doesn't
            contain the aisle or say "about halfway down" or anything.
            currently disabled.
    """
    tree = html.fromstring(search_raw(search_term, extra_params).content)
    results = tree.cssselect('td.EXLSummary')

    def el_to_txt(e):
        if len(e) > 0:
            txt = e[0].text_content()
            return '' if txt is None else txt.strip()
        else:
            return ''

    def fix_call(call_number):
        return call_number.strip('() \t\r\n')

    ret = []
    for result in results:
        availability = result.cssselect('em.EXLResultStatusAvailable')[0]
        summary = result.cssselect('div.EXLSummaryFields')[0]

        exl_prefix = 'span.EXLAvailability'

        item = {
            'library':     availability.cssselect(exl_prefix + 'LibraryName'),
            'collection':  availability.cssselect(exl_prefix + 'CollectionName'),
            'call':        availability.cssselect(exl_prefix + 'CallNumber'),
            'title':       summary.cssselect('h2.EXLResultTitle > a'),
            'author':      summary.cssselect('h3.EXLResultAuthor'),
            'details':     summary.cssselect('span.EXLResultDetails'),
            'year':        summary.cssselect('h3.EXLResultFourthLine'),
        }

        if len(item['call']) == 0:
            continue

        item.update({k: el_to_txt(v) for k, v in item.items()})
        item['call'] = fix_call(item['call'])

        add_directions(item)

        ret.append(item)

        if len(ret) >= max_count:
            break

    return ret

def pretty(item):
    ret = []
    ret.append('{title} ({year}, {author})'.format(**item))
    ret.append('{building} {floor}, {aisle}: {call}'.format(
        call=item['call'],
        **item['directions']))
    return '\n'.join(ret)

def get_directions(
        search_term,
        amount=1,
        numbered=False,
        width=78,
        raw=False,
        number_postfix='. ',
        indent=8,
        separators=False,
        verbose=False,
        continue_numbering=False,
        suppress=False,
        extra_search_params={}
        ):

    ret = []
    results = []
    total_results = 0

    for search_t in search_term:
        search_results = search(search_t, amount, extra_search_params)
        total_results += len(search_results)
        results.append(search_results)

    if total_results == 0:
        misc.err_exit('no results!')
    elif total_results == 1 and not numbered:
        raw = True
    elif not raw or numbered or (total_results > 1 and not raw):
        numbered = True
        number_col_w = misc.digits(total_results) + len(number_postfix)

    i = 1

    if suppress:
        ret = []
        for result_group in results:
            ret.extend(result_group)
        return ret

    for search_t, search_results in zip(search_term, results):
        if separators:
            ret.append('\n' + ' ' * indent + search_t.upper())
            ret.append(       ' ' * indent + '-' * len(search_t))
        if not continue_numbering:
            i = 1
        for result in search_results:
            if verbose:
                ret.append(str(result))
            if numbered:
                ret.append(misc.format_left(
                    pretty(result),
                    firstline=(str(i) + number_postfix).rjust(number_col_w),
                    reformat=False,
                    width=width))
            else:
                ret.append(pretty(result))
            i += 1

    return '\n'.join(ret)

def args_search(args):
    args_dict = args.__dict__
    del args_dict['func']
    return get_directions(**args_dict)

def search_from_bib(bib):
    magic = '1219566' # ???

    bib2onesearch = {
        'freeText': {
            'title': 'title',
            'author': 'creator',
            'keywords': 'sub',
            'issn': 'issn',
            'isbn': 'isbn',
            'publisher': 'lsr02',
        },
        'elsewhere': {
            'year': 'vl(drStartYear7)',
            'endyear' : f'vl({magic}22UI7)',
            'language': f'vl({magic}10UI6)',
        }
    }

    n = 0
    def fill_free(subj, txt):
        nonlocal n
        nonlocal params
        if n > 3:
            return

        n_magic = {
            0: f'vl({magic}13UI0)',
            1: f'vl({magic}15UI1)',
            2: f'vl({magic}16UI2)',
            3: f'vl({magic}18UI3)',
        }

        params[f'vl(freeText{n})'] = txt
        params[n_magic[n]] = subj
        n += 1

    def set_other(key, val):
        nonlocal params
        if key == 'year':
            params[bib2onesearch['elsewhere']['year']] = val
            params[bib2onesearch['elsewhere']['endyear']] = val + 1
        elif key == 'language':
            params[bib2onesearch['elsewhere']['language']] = val

    params = {
        'mode': 'Advanced',
        'vl(1UIStartWith0)': 'exact',
        'vl(1UIStartWith1)': 'exact',
        'vl(1UIStartWith2)': 'exact',
        'vl(1UIStartWith3)': 'exact',
        'vl(boolOperator0)': 'AND',
        'vl(boolOperator1)': 'AND',
        'vl(boolOperator2)': 'AND',
        'vl(boolOperator3)': 'AND',
    }

    # keys ranked by specificity
    rank = [
        'isbn',
        'issn',
        'title',
        'author',
    ]

    # fill priority items first
    for item in rank:
        if item in bib:
            fill_free(bib2onesearch['freeText'][item], bib[item])

    # fill in gaps next
    for bibkey, OneSearch in bib2onesearch['freeText'].items():
        if n == 4:
            break
        elif bibkey in bib:
            fill_free(OneSearch, bib[bibkey])

    for bibkey in bib2onesearch['elsewhere'].keys():
        if bibkey in bib:
            set_other(bibkey, bib[bibkey])

    return params

def bib_search(args):
    ret = []
    for bibtex in args.bibtex_file:
        with open(bibtex) as bib:
            citations = bibtex.parser.parse_string(bib.read())
            for citation in citations:
                params = search_from_bib(citation)
                ret.append(get_directions(
                    [''],
                    extra_search_params=params,
                    **args.__dict__))
    return '\n'.join(ret)

def main():
    parser = argparse.ArgumentParser(
        description='Find materials in the Brandeis Goldfarb / Farber libraries.',
    )

    parser.add_argument('-a', '--amount', type=int, metavar='N', default=1,
        help='parse N results (max 10)')
    parser.add_argument('-n', '--numbered', action='store_true',
        help='format output as a numbered list')
    parser.add_argument('-w', '--width', type=int, default=78,
        help='output width')
    parser.add_argument('-r', '--raw', action='store_true',
        help='raw output; don\'t wrap text')
    parser.add_argument('--number-postfix', default='. ', metavar='STRING',
        help='string to output after the number in numbered output')
    parser.add_argument('-s', '--separators', action='store_true',
        help='output headers between search terms')
    parser.add_argument('-c', '--continue-numbering', action='store_true',
        help='don\'t reset list numbering between search terms')
    parser.add_argument('--verbose', action='store_true',
        help='verbose / debug output; print dicts as well as formatted output')
    parser.add_argument('--suppress', action='store_true',
        help='don\'t output formatted data; useful with --verbose')

    subparsers = parser.add_subparsers()

    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('search_term', nargs='+',
        help='search term passed directly to OneSearch, '
        'search.library.brandeis.edu. can be a call number, title, or author')
    search_parser.set_defaults(func=args_search)

    bib_parser = subparsers.add_parser('bib')
    bib_parser.add_argument('bibtex_file', nargs='+',
        help='bibtex file to process; only references title fields')
    bib_parser.set_defaults(func=bib_search)

    args = parser.parse_args()

    print(args.func(args))

if __name__ == '__main__':
    main()
