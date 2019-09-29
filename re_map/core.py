import re
from .utils import decorate

__verbose__ = False
__extended__ = False

def span_len_delta(span_1, span_2):
    return (span_1[1] - span_1[0]) - (span_2[1] - span_2[0])

def len_delta(match_start, replacement_span_map):
    delta = 0
    for span_source, span_target in replacement_span_map:
        if span_target[1] <= match_start:
            delta += span_len_delta(span_target, span_source)

    return delta

def validate(entry_1, i, replacement_span_map):
    if len(replacement_span_map) <= i or i < 0:
        return

    entry_2 = replacement_span_map[i]

    # uses assum[ption that span[0] < span[1]
    ops = [
        lambda x, y : (x[0] < y[0]) == (x[1] < y[0]),
        lambda x, y : (x[0] > y[0]) == (x[0] > y[1]),
        lambda x, y : (x[0] == y[0]) == (x[1] == y[1])
    ]

    def cmp(span1, span2):
        valid = True
        for op in ops:
            valid = valid and op(span1, span2)
        return valid

    valid = cmp(entry_1[0], entry_2[0])
    valid = valid and cmp(entry_1[1], entry_2[1])

    #if not valid:
    #    raise Exception("New entry intersects with other entry")

def sub(span, value):
    return span[0] - value, span[1] - value

def insert(entry, current_span, replacement_span_map):
    delta = span_len_delta(entry[1], entry[0])

    i=0
    replace=False
    for i in range(len(replacement_span_map) + 1): # +1 for i to actually reach last element
        if i == len(replacement_span_map):
            break
        if replacement_span_map[i][0][0] > entry[0][1]:
            break
        if replacement_span_map[i][0] == entry[0]:
            replace = True
            break

    if replace:
        entry = replacement_span_map[i][0], entry[1]
        del replacement_span_map[i]

    validate(entry, i - 1, replacement_span_map)
    replacement_span_map.insert(i, entry)
    validate(entry, i + 1, replacement_span_map)

    for j in range(i+1, len(replacement_span_map)):
        replacement_span_map[j] = replacement_span_map[j][0], (replacement_span_map[j][1][0] + delta, replacement_span_map[j][1][1] + delta)

    return delta

def repl(match, replacement_map, replacement_span_map):
    match_string = match.group()
    match_start = match.span(0)[0]
    delta = len_delta(match.span(1)[0], replacement_span_map)
    
    current_match_delta = 0
    
    for i in replacement_map.keys():
        span = match.span(i)
        group_rel_span = span[0] - match_start, span[1] - match_start

        replacement = replacement_map[i] if isinstance(replacement_map[i], str) else replacement_map[i](match.group(i))
        match_string = match_string[0:group_rel_span[0] + current_match_delta] + replacement + match_string[group_rel_span[1] + current_match_delta:]

        match_delta = delta + current_match_delta
        group_rel_span_alligned = group_rel_span[0] + match_delta, group_rel_span[1] + match_delta

        span_target = group_rel_span_alligned[0] + match_start, group_rel_span_alligned[0] + len(replacement) + match_start
        assert(span_target[0] <= span_target[1])
        
        new_entry = span, span_target
        
        current_match_delta += insert(new_entry, span, replacement_span_map)

    return match_string

def update_span_map(replacement_span_map, tmp_replacement_span_map):
    return tmp_replacement_span_map

def process(text, modifiers):
    processed_text = str(text)
    replacement_span_map = []

    for i in range(len(modifiers)):
        tmp_replacement_span_map = []
        pattern, replacement_map = modifiers[i]

        if(__verbose__):
            print ('in:', processed_text, i)

        processed_text = re.sub(
            pattern = pattern,
            repl = lambda match: repl(match, replacement_map, tmp_replacement_span_map),
            string = processed_text
        )

        replacement_span_map = update_span_map(replacement_span_map, tmp_replacement_span_map)

        if(__verbose__):
            decorate(text, processed_text, replacement_span_map)
            print ( replacement_span_map )
            print ('out:', processed_text, i)

        if __extended__:
            pass

    return processed_text, replacement_span_map
