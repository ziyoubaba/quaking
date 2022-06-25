#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
import numpy
from freetype import *
import OpenGL.GL as gl

import os

FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")

base, texid = 0, 0


def makefont(filename, size, pos_x=0, pos_y=0):
    global texid

    # Load font  and check it is monotype
    face = Face(filename)
    face.set_char_size(size * 64)
    # if not face.is_fixed_width:
    #     raise 'Font is not monotype'

    # Determine largest glyph size
    width, height, ascender, descender = 0, 0, 0, 0
    for c in range(32, 128):
        face.load_char(chr(c), FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT)
        bitmap = face.glyph.bitmap
        width = max(width, bitmap.width)
        ascender = max(ascender, face.glyph.bitmap_top)
        descender = max(descender, bitmap.rows - face.glyph.bitmap_top)
    height = ascender + descender

    # Generate texture data
    Z = numpy.zeros((height * 6, width * 16), dtype=numpy.ubyte)
    for j in range(6):
        for i in range(16):
            face.load_char(chr(32 + j * 16 + i), FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            x = i * width + face.glyph.bitmap_left
            y = j * height + ascender - face.glyph.bitmap_top
            Z[y:y + bitmap.rows, x:x + bitmap.width].flat = bitmap.buffer

    # Bound texture
    texid = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texid)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_ALPHA, Z.shape[1], Z.shape[0], 0, gl.GL_ALPHA, gl.GL_UNSIGNED_BYTE, Z)

    # Generate display lists
    dx, dy = width / float(Z.shape[1]), height / float(Z.shape[0])
    base = gl.glGenLists(8 * 16)
    gl.glEnable(gl.GL_TEXTURE_2D)
    for i in range(8 * 16):
        c = chr(i)
        x = i % 16
        y = i // 16 - 2
        gl.glNewList(base + i, gl.GL_COMPILE)
        if (c == '\n'):
            gl.glPopMatrix()
            gl.glTranslatef(0, -height, 0)
            gl.glPushMatrix()
        elif (c == '\t'):
            gl.glTranslatef(4 * width, 0, 0)
        elif (i >= 32):
            # gl.glBegin( gl.GL_QUADS )
            # gl.glTexCoord2f( (x  )*dx, (y+1)*dy ), gl.glVertex3f( 0,     -height, 0 )
            # gl.glTexCoord2f( (x  )*dx, (y  )*dy ), gl.glVertex( 0,     0 )
            # gl.glTexCoord2f( (x+1)*dx, (y  )*dy ), gl.glVertex( width, 0 )
            # gl.glTexCoord2f( (x+1)*dx, (y+1)*dy ), gl.glVertex( width, -height )
            # gl.glEnd( )
            # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f((x) * dx, (y) * dy);
            gl.glVertex3f(pos_x, pos_y, 0)
            gl.glTexCoord2f((x + 1) * dx, (y) * dy);
            gl.glVertex3f(pos_x + width, pos_y, 0)
            gl.glTexCoord2f((x + 1) * dx, (y + 1) * dy);
            gl.glVertex3f(pos_x + width, pos_y + height, 0)
            gl.glTexCoord2f((x) * dx, (y + 1) * dy);
            gl.glVertex3f(pos_x, pos_y + height, 0)
            gl.glEnd()
            gl.glTranslatef(width, 0, 0)
        gl.glEndList()


def display(text, size=16, pos_x=0, pos_y=0, color=(0,0,0,255)):
    # gl.glTexEnvf( gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE )
    # gl.glEnable( gl.GL_DEPTH_TEST )
    # gl.glEnable( gl.GL_BLEND )
    # gl.glEnable( gl.GL_COLOR_MATERIAL )
    # gl.glColorMaterial( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE )
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    makefont(FONT, size, pos_x=pos_x, pos_y=pos_y)

    global texid
    # gl.glClearColor(1,1,1,1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texid)
    gl.glColor4ub(*color)
    gl.glPushMatrix()
    gl.glListBase(base + 1)
    gl.glCallLists([ord(c) for c in text])
    gl.glPopMatrix()
