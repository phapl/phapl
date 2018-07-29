# -*- coding: utf-8 -*-
# insert cache

import sys
import string

h = sys.stdin.read()

lang = sys.argv[1]

with open('generated_js_part.' + lang + '.js.lzma.base64') as f:
    pre_cache = f.read()

h = string.Template(h)
h = h.safe_substitute(
    compressed_cache_base64 = pre_cache,
    )

sys.stdout.write(h)
