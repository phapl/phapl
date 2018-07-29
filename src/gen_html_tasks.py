# -*- coding: utf-8 -*-
# Generate html to embed list of tasks into phapl.html

import sys
import codecs
import locale
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

import json

import libphapl

k = 0

for_cache = []

def format_file(fname):
    global k
    k += 1
    title = None
    author = None
    comment = None
    tasks = []
    with open(fname) as f:
        for l in f:
            # l = l.decode('utf-8')
            l = l.strip()
            t = "Title: "
            if l.startswith(t):
                title = l[len(t) : ]
                continue
            t = "Author: "
            if l.startswith(t):
                author = l[len(t) : ]
                continue
            t = "Comment: "
            if l.startswith(t):
                comment = l[len(t) : ]
                continue
            tasks.append(l)
    title = title.decode('utf-8')
    author = author.decode('utf-8')
    if comment != None:
        comment = comment.decode('utf-8')
    # print '<div class="container">'
    print '<div>'
    # %% do we need action="#" here?
    print '<form>'
    print u'''<input type="button" id="block{0}-header" onclick="collapse('block{0}')" value="&#9658; [[Показать задачи | Show tasks]]: {1}">'''.format(k, title)
    print '<div id="block{0}" style="display: none">'.format(k)
    if author == None:
        print u'[[Автор не известен | Author is unknown.]].<br>'
    else:
        print u'' + author + '</br>'
    if comment != None:
        print u'<b>[[Комментарии | Comments]]:</b> ' + comment + '</br>'
    # %% hardcoded 30: 3 * 10
    print '<table border="1" style="border-collapse: collapse;">'
    for ii in range(10):
        print '<tr>'
        for j in range(3):
            i = j * 10 + ii
            t = tasks[i]
            dot_foo = [ u.strip('" ') for u in t.split(',') ]
            # print dot_foo
            d = libphapl.task_to_json(*dot_foo)
            html, js = libphapl.make_html(d)
            for_cache.append([ dot_foo, html, js ])
            t = t.replace('"', "'")
            # %% save original order of elements in formula?
            # %% ln() becomes log(), save ln() ?
            tt = (r'\( \left\{ \begin{aligned}'
                  + r'\dot{x} &= ' + d['dot_x_tex'] + r' \\'
                  + r'\dot{y} &= ' + d['dot_y_tex']
                  + r' \end{aligned}\right. \)')
            print '<td onclick="phapl_set(this, {})">{}. {}</td>'.format(t, i + 1, tt)
        print '</tr>'
    # print '<script type="text/javascript">'
    # print 'phapl_populate_cache("' + t + '");'
    # print '</script>'
    print '</table>'
    print '</form>'
    print '</div>'
    print '</div>'

with open('js_common.html_part', 'w') as f:
    f.write(libphapl.js_common.encode('utf-8'))

for f in sys.argv[1 : ]:
    format_file(f)

for l in for_cache:
    l[0] = '"{}", "{}"'.format(*l[0])

t = json.dumps(for_cache)
with open('generated_js_part.js', 'w') as f:
    f.write(t)
