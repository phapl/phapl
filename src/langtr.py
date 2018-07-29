# -*- coding: utf-8 -*-
# script to expand markup for translations

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

import sys
import re
import json

languages = [ 'ru', 'en' ]

def make_replacer(i):
    def f(m):
        t = m.group(1).split(' | ')
        assert len(t) == len(languages), m.group(0)
        return t[i]
    return f

def replace(s, i):
    lang = languages[i]
    c = re.sub(r'\[\[([^]]*)\]\]', make_replacer(i), s)
    if '[[' in c:
        t = c.index('[[')
        print 'Warning: [[ in ' + lang + ' version'
        print '  ', repr(c[max(0, t - 10) : t + 10])
    if ']]' in c:
        t = c.index(']]')
        print 'Warning: ]] in ' + lang + ' version'
        print '  ', repr(c[max(0, t - 10) : t + 10])
    if lang == 'en':
        t = c.replace('©', '')
        t = t.replace('Language / язык', '')
        t = t.replace('Русский', '')
        m = re.search(r'[\x7f-\xff]', t)
        if m:
            t = m.start()
            print 'Warning: non-ascii in ' + lang + ' version'
            print '  ', repr(c[max(0, t - 10) : t + 10])
    return c

def save(contents, o_fmt, lang):
    n = o_fmt.format(lang)
    assert o_fmt != n
    with open(n, 'wb') as f:
        f.write(contents)

def tr_static(ifile, o_fmt):
    contents = ifile.read()
    ifile.close()
    for i, lang in enumerate(languages):
        c = replace(contents, i)
        save(c, o_fmt, lang)

def tr_json(ifile, o_fmt):
    o = json.load(ifile)
    # we support only list of lists of strings
    assert type(o) == list
    for i, lang in enumerate(languages):
        r = []
        for e in o:
            assert type(e) == list
            l = []
            for t in e:
                assert type(t) == unicode
                # %% remove encode/decode, they should not be needed
                t = t.encode('utf-8')
                t = replace(t, i)
                t = t.decode('utf-8')
                l.append(t)
            r.append(l)
        t = json.dumps(r)
        save(t, o_fmt, lang)

if __name__ == '__main__':
    if sys.argv[1] == 'static':
        o_fmt = sys.argv[2]
        assert len(sys.argv) == 3
        tr_static(sys.stdin, o_fmt)
    elif sys.argv[1] == 'json':
        o_fmt = sys.argv[2]
        assert len(sys.argv) == 3
        tr_json(sys.stdin, o_fmt)
        # assert len(sys.argv) == 2
        # tr_json(sys.stdin, sys.stdout)
    else:
        print 'Usage:'
        print '  ... static format_string_for_names_of_output_files < input_file'
        print '  ... json format_string_for_names_of_output_files < input_file'
        print '    json should have very limited structure;'
        # print '  ... json < input.json > output.json'
        # print '   output will be [ old json object with placeholders, dict ]'
