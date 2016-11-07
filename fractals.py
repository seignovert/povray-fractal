#!/bin/python
# Fractals aggregates database and drawing
# Author B. Seignovert
# univ-reims@seignovert.fr
# V2.0 - 2016/04/29
# -*- coding: utf-8 -*-

import numpy as np
import os,sys

class DB:
    def __init__(self,root,name):
        import sqlite3 as sqlite

        self.name      = name
        self.root      = root
        self.db        = root + name
        self.connexion = sqlite.connect(self.db)
        self.cursor    = self.connexion.cursor()
        return
    
    def __repr__(self):
        return "Fractal Database Object. Location: %s" % self.db

    def create(self,n):
        self.cursor.execute("DROP TABLE IF EXISTS Geo_%i" % n)
        self.cursor.execute( "CREATE TABLE Geo_%i(\n" % n +\
                             "k\tINTEGER,\n" +\
                             "x\tREAL,\n"    +\
                             "y\tREAL,\n"    +\
                             "z\tREAL \n"    +\
                             ");" )
        self.connexion.commit()
        return

    def load(self,n):
        fname = 'Part%i' % n
        k = 0; i = n; data = []
        with open(fname) as f:
            for line in f.readlines():
                if i == n:
                    i  = 0
                    k += 1
                else:
                    i += 1
                    xyz = line.strip().split()
                    data.append( [ k, float(xyz[0]), float(xyz[1]), float(xyz[2]) ] )

        return data

    def save(self,n):
        self.create(n)
        self.cursor.executemany("INSERT INTO Geo_%i VALUES (?,?,?,?)" % n, self.load(n) )
        self.connexion.commit()
        return

    def get(self,n,k):
        self.cursor.execute("SELECT x,y,z FROM Geo_%i WHERE k=%i" % (n,k) )
        return self.cursor.fetchall()

    def getExtend(self,n,k):
        self.cursor.execute("SELECT MAX(ABS(x)),MAX(ABS(y)),MAX(ABS(z)) FROM Geo_%i WHERE k=%i" % (n,k))
        return self.cursor.fetchone()
    
class DRAW:
    def __init__(self,n=128,k=1,radius=.5):
        import vapory as pov

        self.pov = pov
        self.n   = n
        self.k   = k
        self.r   = radius
        self.create()
        return

    def __repr__(self):
        return "Fractal aggregate of %i momoners (index: %i)" % (self.n,self.k)

    def create(self):
        self.obj = [ self.pov.LightSource([1000,1000,-5000], 'color',1) ]
        self.extend = 0
        return

    def add(self,x,y,z, color=[256,150,0] ):
        self.obj.append( self.pov.Sphere( [x,y,z], self.r, self.pov.Texture( self.pov.Pigment('color', np.array(color)/256.), self.pov.Finish('diffuse',1, 'phong',.3) )))
        if abs(x) > self.extend:
            self.extend = abs(x)
        if abs(y) > self.extend:
            self.extend = abs(y)
        if abs(z) > self.extend:
            self.extend = abs(z)
        return

    def save(self, width=900, height=600, zoom=None, antialiasing=0.001, fname=None ):
        if zoom is None:
            zoom = 140*self.extend
        if fname is None:
            fname = 'Fractal_%i-%i.png' % (self.n,self.k)

        camera = self.pov.Camera( 'angle', 1, 'location', [zoom,0,-zoom], 'look_at', [0,0,0])
        scene  = self.pov.Scene( camera, self.obj, included=['colors.inc', 'textures.inc'])
        
        scene.render(fname , width=width, height=height, antialiasing=antialiasing)
        print '> %s saved in %s' % (self,fname)
        return
