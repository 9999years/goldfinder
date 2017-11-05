import requests
import argparse
from urllib import parse as urlparse
from lxml import html
import re

def search_raw(search_term):
    params = {
        'mode': 'Basic',
        'vid': 'BRAND',
        'vl(freeText0)': search_term,
        'fn': 'search',
        'tab': 'alma',
    }

    url = 'http://search.library.brandeis.edu/primo_library/libweb/action/search.do'

    return requests.get(url, params=params)

def search(search_term):
    tree = html.fromstring(search_raw(search_term).content)
    results = tree.cssselect('td.EXLSummary')

    def el_to_txt(e):
        txt = e[0].text_content()
        return '' if txt is None else txt.strip()

    def fix_call(call_number):
        return call_number.strip('() \t\r\n')

    ret = []
    for result in results:
        # <p class="EXLResultAvailability">
        # <em class="EXLResultStatusAvailable" id="RTADivTitle_0">
        # Available at <span class="EXLAvailabilityLibraryName">
        # Main Library</span>&nbsp;
        # <span class="EXLAvailabilityCollectionName">
        # Stacks</span>&nbsp;
        # <span class="EXLAvailabilityCallNumber">
        # (B3305.M74 C56 2004 )</span><span id="RTASpan_0">()</span> </em>

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

        ret.append(item)
    return ret

def floor(item):
    url = urlparse.urlparse(item['directions']['maps'][0]['mapurl'])
    params = urlparse.parse_qs(url.query)
    floor = params['floor'][0]
    return 'M' if floor == '5' else int(floor)

def building(item):
    # something like: Please proceed to the mezzanine level of the Goldfarb
    # building of the Brandeis University Library.
    directions = item['directions']['maps'][0]['directions']
    return re.match('(Goldfarb|Farber) building', directions)

def directions(item):
    if 'directions' in item:
        return

    params = {
        'holding[]': '{library}$${collection}$${call}'.format(**item),
        'alt': 'true',
    }

    url = 'https://brandeis.stackmap.com/json/'

    item.update({'directions': requests.get(
        url, params=params).json()['results'][0]})

    item['directions']['floor'] = floor(item)

def top(search_term):
    return search(search_term)[0]

def pretty(item):
    ret = []
    ret.append('{title} ({year}, {author})'.format(**item))
    return ''.join(ret)

def simple():
    marx = top('marx')
    directions(marx)
    # print(pretty(marx))
    return marx

def main():
    parser = argparse.ArgumentParser(
        description='Find materials in the Brandeis Goldfarb / Farber libraries.',
    )

    parser.add_argument('search_term', nargs='+')
    args = parser.parse_args()

    results = search(search_term)
    for result in results:
        print('{title} ({year}, {author})'.format(result))
        print('----------')

if __name__ == 'main':
    main()
