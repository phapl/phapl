# -*- coding: utf-8 -*-
# Generate html from parts with phapl.html

import sys
import string
import time

# with open('phapl_tpl.html') as f:
#     h = f.read()
h = sys.stdin.read()

with open('task_containers.html_part') as f:
    embed = f.read()

with open('js_common.html_part') as f:
    js_common = f.read()

h = string.Template(h)
h = h.safe_substitute(
    task_containers = embed,
    js_common = js_common,
    date = time.strftime('%Y-%m-%d %H:%M %z')
    )

sys.stdout.write(h)
