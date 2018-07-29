# PhaPl

EN: PhaPl is a software to research and plot phase portraits of autonomous systems of 2 differential equations on a plane. PhaPl works as a site or as a local html-page that works offline.

RU: PhaPl - программное обеспечение для автоматического построения и исследования фазовых портретов автономных динамических систем на плоскости. PhaPl работает как сайт или как локальная html-страница, не требующая подключения к сети Интернет.

## Online

https://phapl.github.io/

## Offline

[Download](https://github.com/phapl/phapl.github.io/archive/master.zip) (~9 MB download, ~37 unpacked)

## Licenses

### Non-free tasks

PhaPl includes non-free tasks (`tasks_mainpdf_kz16.txt` and `tasks_mainpdf_kz17.txt`) that cannot be redistributed due to copyright.

`Copyright © 2010 Astashova I.V., Nikishkin V.A.`

Асташова И. В., Никишкин В. А. Практикум по курсу «Дифференциальные уравнения». Учебное пособие. Изд. 3-е, исправленное. М.: Изд. центр ЕАОИ, 2010. 94 с., ил.

Astashova I.V., Nikishkin V.A. Practicum on course "Differential equations". Tutorial. 3rd edition, revised. Moscow: Publishing Center of EOI, 2010. 94 p., illustrated.

http://new.math.msu.su/diffur/main_du_2010.pdf

The tasks are "compiled" into the result and make `phapl.ru.html` and `phapl.en.html` non-redistributable too.

### PhaPl itself, except non-free tasks

PhaPl is a Free Software. In practice, generated `phapl.ru.html` and `phapl.en.html` are not redistributable due to built-in non-free tasks. With other sets of tasks, it may be redistributable.

`Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>`

`Redistribution and use in source and binary forms, with or without modification, are permitted.`

### Modified SymPy, PyPy.js, MathJax, LZMA-JS

PhaPl includes and uses awesome Free Software made by other authors. Packaging is fully automated and repeatable. `build.sh` downloads everything and applies required modifications:

- a few fixes for SymPy to work under PyPy.js

- cleanups for SymPy and modules included within PyPy.js

- cleanups for MathJax to reduce the size

[LZMA-JS](https://github.com/LZMA-JS/LZMA-JS)

[PyPy.js](https://github.com/pypyjs/pypyjs)

[MathJax](https://github.com/mathjax/MathJax)

[SymPy](https://www.sympy.org/en/index.html) (downloaded using `pip`)

## Previous version

For historic purposes, there is [older version](https://github.com/AlekseyCherepanov/phapl) of PhaPl.
