#!/bin/python
# Draw fractal aggregates
# Author B. Seignovert
# univ-reims@seignovert.fr
# V1.1 - 2016/04/29
# -*- coding: utf-8 -*-

import os,sys
import numpy as np

from fractals import DB, DRAW

n = 128
k = 1
r = 10

if len(sys.argv) > 1:
    n = int(sys.argv[1])
if len(sys.argv) > 2:
    k = int(sys.argv[2])
if len(sys.argv) > 3:
    r = int(sys.argv[3])

db  = DB('','fractals.db')

for rr in range(r):
    ang = np.radians(rr*360./r)
    agg = DRAW(n,k)
    for (x,y,z) in db.get(n,k):
        agg.add(x*np.cos(ang)-z*np.sin(ang),y,x*np.sin(ang)+z*np.cos(ang))

    agg.save(width=750,height=750,zoom=750,fname='Fractal_%i-%i-rot-%.2i' % (n,k,rr))
