#! /bin/sh
# Build PhaPl site from zero downloading everything needed
# !>! It downloads code from github and runs it (pypy.js' bundler).
# >!> It invokes pip to install sympy.
# !>! It puts temporary files in current dir.
# Results will be in site/ .
# TODO: it can try to install isympy script. Really? Where? Prevent it.

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without modification, are permitted.

die() {
    printf 'FAILURE: %s\n' "$1"
    exit 1
}

rm -rf site/lib
mkdir -p site/lib || die "can't create site/lib/ folder"

BASE=$(dirname "$0")


# LZMA-JS

wget -nc https://github.com/LZMA-JS/LZMA-JS/archive/v2.3.0.tar.gz || die 'wget lzma-js'

rm -rf LZMA-JS-2.3.0
tar xzf v2.3.0.tar.gz LZMA-JS-2.3.0/src/lzma-d-min.js
mv LZMA-JS-2.3.0/src/lzma-d-min.js site/lib || die 'mv'


# PyPy.js, nojit

wget -nc https://github.com/pypyjs/pypyjs/releases/download/v0.4.0/pypyjs-nojit-0.4.0.tar.gz || die 'wget pypy.js'

rm -rf pypyjs-nojit-0.4.0
tar xzf pypyjs-nojit-0.4.0.tar.gz || die 'unpacking pypyjs'

(cd pypyjs-nojit-0.4.0/lib/ && cp FunctionPromise.js Promise.min.js pypyjs.vm.js pypyjs.js pypyjs.vm.js.zmem ../../site/lib/) || die 'cp pypy'

cp -r pypyjs-nojit-0.4.0/lib/modules/ site/lib/ || die 'cp pypy 2'


# for GitHub Pages: disable smart rendering
touch site/.nojekyll


# generate html part of PhaPl

# %% message about slow work
python "$BASE"/gen_html_tasks.py "$BASE"/tasks_mainpdf_kz16.txt "$BASE"/tasks_mainpdf_kz17.txt > task_containers.html_part || die 'gen_html_tasks.py'

python "$BASE"/langtr.py json 'generated_js_part.{}.js' < generated_js_part.js && for l in ru en ; do lzma -9 < generated_js_part.$l.js > generated_js_part.$l.js.lzma && base64 generated_js_part.$l.js.lzma | perl -C0 -pe 's/\s+//' > generated_js_part.$l.js.lzma.base64 ; done

(cd site && (cd ../ && python "$BASE"/gen_html_combine.py < "$BASE"/phapl_tpl.html) | python "$BASE"/langtr.py static '../phapl.{}.html' && (cd ../ && python "$BASE"/gen_html_combine2.py ru < phapl.ru.html) > phapl.ru.html && (cd ../ && python "$BASE"/gen_html_combine2.py en < phapl.en.html) > phapl.en.html)

# static html
cp "$BASE"/index.html "$BASE"/phapl.html site/


# MathJax, and cleaning/shrinking

wget -nc https://github.com/mathjax/MathJax/archive/2.5.3.tar.gz || die 'wget mathjax'

rm -rf MathJax-2.5.3
tar xzf 2.5.3.tar.gz || die 'unpacking mathjax'

(cd MathJax-2.5.3 && ( mv ./fonts/HTML-CSS/TeX/woff . && rm -r fonts/* && mkdir -p fonts/HTML-CSS/TeX/ && mv woff fonts/HTML-CSS/TeX/ ) && rm -r jax/output/SVG && rm -r unpacked docs config/A* config/d* config/local config/Safe.js config/M* config/TeX-AMS_HTML-full.js config/TeX-AMS-MML_SVG-full.js config/TeX-AMS_HTML.js config/TeX-AMS-MML_SVG.js config/TeX-AMS-MML_HTMLorMML-full.js  config/TeX-MML-AM_HTMLorMML-full.js config/TeX-MML-AM_HTMLorMML.js && rm .gitignore)

mv MathJax-2.5.3 site/lib/mathjax || die 'mv'


# SymPy

rm -rf pylibs
pip install sympy==0.7.6.1 -t pylibs

find pylibs/sympy -name '*.pyc' -delete

rm -rf pylibs/sympy/utilities/mathml/data
rm -rf pylibs/sympy/logic/benchmarks/input

sed -i -e 's/from .runtests import test, doctest/# &/' pylibs/sympy/utilities/__init__.py

sed -i -e 's/from threading import RLock/\n# &\nclass RLock(object):\n    def __enter__(*args):\n        pass\n    def __exit__(*args):\n        pass/' pylibs/sympy/core/compatibility.py

# drop BOM; PyPy.js cannot handle it
perl -C0 -0777 -i -pe 's/^\xef\xbb\xbf//' pylibs/sympy/solvers/solvers.py

#mv pylibs/sympy site/lib/modules/ || die 'mv sympy'

python pypyjs-nojit-0.4.0/tools/module_bundler.py add site/lib/modules pylibs/sympy

python pypyjs-nojit-0.4.0/tools/module_bundler.py preload site/lib/modules distutils
#python pypyjs-nojit-0.4.0/tools/module_bundler.py add site/lib/modules site/lib/modules/sympy/


# Installing python part of PhaPl

# %% make function?
# for libphapl.py
perl -CSDA -pe 's/[^\x00-\x7f]/sprintf "\\u%04x", ord $&/ge' < "$BASE"/libphapl.py > site/lib/modules/libphapl.py && python pypyjs-nojit-0.4.0/tools/module_bundler.py add site/lib/modules site/lib/modules/libphapl.py && python pypyjs-nojit-0.4.0/tools/module_bundler.py preload site/lib/modules libphapl
# and for tg1.py:
perl -CSDA -pe 's/[^\x00-\x7f]/sprintf "\\u%04x", ord $&/ge' < "$BASE"/tg1.py > site/lib/modules/tg1.py && python pypyjs-nojit-0.4.0/tools/module_bundler.py add site/lib/modules site/lib/modules/tg1.py && python pypyjs-nojit-0.4.0/tools/module_bundler.py preload site/lib/modules tg1

# for quick updates add the following:
# && python pypyjs-nojit-0.4.0/tools/module_bundler.py remove site/lib/modules libphapl
# python pypyjs-nojit-0.4.0/tools/module_bundler.py remove site/lib/modules tg1 &&


# Cleaning up modules in PyPy.js

rm site/lib/modules/test/test_*
rm site/lib/modules/test/*test*
find site/lib/modules/ -name 'tests' -print0 | xargs -0 rm -rf
find site/lib/modules/ -name 'benchmarks' -print0 | xargs -0 rm -rf
#rm site/lib/modules/email/test/test_*
rm -r site/lib/modules/email
rm site/lib/modules/test/leakers/test_*
rm site/lib/modules/unittest/test/test_*

# TODO: should we keep the following files?
# ./unittest/test/test_runner.py
# ./unittest/test/test_program.py


# for GitHub Pages: enlist _* files to be served too
# TODO: proper quoting of names
(cd site && find . -name '_*' | perl -C0 -pe 's/\n//; s/^/"/; s/$/", /' | perl -C0 -pe 's/^/include: [/; s/, $/]\n/' > _config.yml)
