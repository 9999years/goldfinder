import textwrap
import math

def digits(n):
    return math.floor(math.log10(n)) + 1

def fill(*txt, width=78, joiner='\n\n', **kwargs):
    def fill_fn(msg):
        return textwrap.fill(msg, width=width, **kwargs)
    return joiner.join(map(fill_fn, ''.join(txt).split(joiner)))

def format_left(txt, leader='', width=78, firstline=None, align_leader='right',
        reformat=True):
    firstline = firstline or leader
    margin = len(firstline)
    leader = leader.rjust(margin) if align_leader == 'right' else leader
    width = width - margin

    lines = []
    if reformat:
        lines = textwrap.wrap(txt, width=width)
    else:
        for l in txt.splitlines():
            lines.extend(textwrap.wrap(l, width=width))

    out = [f'{firstline}{lines.pop(0)}']
    for line in lines:
        out.append(f'{leader}{line}')
    return '\n'.join(out)

def center(txt, width=78, fillchar=' '):
    return txt.center(width, fillchar)

def align(left='', center='', right='', width=78, fillchar=' '):
    """
    returns a string aligned to `width`, with `left`, `right`, and `center` at
    their respective locations in the string. `center` will destructively
    overwrite `left` and `right`, and `left` will overwrite `right`.

    like a stronger left_pad
    """
    lr = left + right.rjust(width, fillchar)[len(left):]

    c = width // 2
    halfc = int(c - len(center) / 2)

    return lr[:halfc] + center + lr[halfc + len(center):]
