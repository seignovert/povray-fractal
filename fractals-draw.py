#!/bin/python
# Draw fractal aggregates
# Author B. Seignovert
# univ-reims@seignovert.fr
# V1.1 - 2016/04/29
# -*- coding: utf-8 -*-

import os,sys

from fractals import DB, DRAW

n = 128
k = 1

if len(sys.argv) > 1:
    n = int(sys.argv[1])
if len(sys.argv) > 2:
    k = int(sys.argv[2])

db  = DB('','fractals.db')
agg = DRAW(n,k)

for (x,y,z) in db.get(n,k):
    agg.add(x,y,z)

agg.save(width=750,height=750,zoom=750)
