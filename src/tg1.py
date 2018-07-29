# -*- coding: utf-8 -*-
# task generator, linear systems

import random
import sympy

squares_set = { 0 }
squares_max = 0
squares_max_i = 0

def squares_fill_up_to(x):
    # x may be negative
    global squares_max
    global squares_max_i
    x = abs(x)
    if x <= squares_max:
        return
    i = squares_max_i
    while True:
        i += 1
        q = i * i
        squares_set.add(q)
        squares_max = q
        squares_max_i = i
        if q > x:
            break

def is_square(x):
    # x may be negative
    x = abs(x)
    if x > squares_max:
        squares_fill_up_to(x)
    return x in squares_set

def get_type(a, b, c, d):
    S = a + d
    D = a * d - b * c
    DD = S ** 2 - 4 * D
    # is square?
    q = '_n'
    if is_square(DD):
        q = '_q'
    else:
        return '_'
    if DD < 0:
        if S == 0:
            return '4' + q
        if S > 0:
            return '5' + q
        if S < 0:
            return '6' + q
        assert 0
    if DD == 0:
        if S < 0:
            if b == 0 and c == 0:
                assert a == d
                assert a < 0
                return '8a' + q
            return '8' + q
        if S > 0:
            if b == 0 and c == 0:
                assert a == d
                assert a > 0
                return '7a' + q
            return '7' + q
        return 'err4'
    assert DD > 0
    if S == 0:
        return '3' + q
    s = S ** 2
    Q = DD
    if s < Q:
        return '3' + q
    if s == Q:
        return 'err2'
    if s > Q:
        if S > 0:
            return '1' + q
        if S < 0:
            return '2' + q
    assert 0

def gen_linear(equilibria_type):
    # type of equilibria -> list 3 items: \dot{x}, \dot{y} formulas as
    # text and system in latex
    # # or None for inability to generate; should not happen
    assert equilibria_type in { '1', '2', '3', '4', '5', '6', '7', '7a', '8', '8a' }, equilibria_type
    t = equilibria_type + '_q'
    l = range(-5, 6)
    r = []
    for a in l:
        for b in l:
            for c in l:
                for d in l:
                    abcd = (a, b, c, d)
                    ss = get_type(*abcd)
                    if t == ss:
                        r.append(abcd)
    assert r != []
    a, b, c, d = random.choice(r)
    dot_x = '{} * x + {} * y'.format(a, b)
    dot_y = '{} * x + {} * y'.format(c, d)
    dot_xy = map(sympy.simplify, (dot_x, dot_y))
    dx, dy = map(sympy.latex, dot_xy)
    r = map(str, dot_xy)
    s = (r'<p>$$ \left\{ \begin{aligned}'
         + r'\dot{x} &= ' + dx + r' \\ '
         + r'\dot{y} &= ' + dy
         + r' \end{aligned}\right. $$</p>')
    # %% line copy-pasted from libphapl; lift?
    s += u'<a href="#" onclick="phapl_gen_linear(\x27{}\x27, false); return false">[[Создать случайную задачу с таким же типом особой точки | Generate random task with the same type of equilibria]]</a><br>'.format(equilibria_type)
    r.append(s)
    return r

# print gen_linear('1')
