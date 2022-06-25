# -*- coding: utf-8 -*-

from __future__ import unicode_literals

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Texture font class

'''
import sys
import math
import numpy as np
import OpenGL.GL as gl
from freetype import *
import os
import ctypes
import numpy as np
import OpenGL.GL as gl

class TextureAtlas:

    def __init__(self, width=1024, height=1024, depth=1):
        '''
        Initialize a new atlas of given size.

        Parameters
        ----------

        width : int
            Width of the underlying texture

        height : int
            Height of the underlying texture

        depth : 1 or 3
            Depth of the underlying texture
        '''
        self.width  = int(math.pow(2, int(math.log(width, 2) + 0.5)))
        self.height = int(math.pow(2, int(math.log(height, 2) + 0.5)))
        self.depth  = depth
        self.nodes  = [ (0,0,self.width), ]
        self.data   = np.zeros((self.height, self.width, self.depth),
                               dtype=np.ubyte)
        self.texid  = 0
        self.used   = 0



    def upload(self):
        '''
        Upload atlas data into video memory.
        '''

        if not self.texid:
            self.texid = gl.glGenTextures(1)

        gl.glBindTexture( gl.GL_TEXTURE_2D, self.texid )
        gl.glTexParameteri( gl.GL_TEXTURE_2D,
                            gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP )
        gl.glTexParameteri( gl.GL_TEXTURE_2D,
                            gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP )
        gl.glTexParameteri( gl.GL_TEXTURE_2D,
                            gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR )
        gl.glTexParameteri( gl.GL_TEXTURE_2D,
                            gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
        if self.depth == 1:
            gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_ALPHA,
                             self.width, self.height, 0,
                             gl.GL_ALPHA, gl.GL_UNSIGNED_BYTE, self.data )
        else:
            gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGB,
                             self.width, self.height, 0,
                             gl.GL_RGB, gl.GL_UNSIGNED_BYTE, self.data )



    def set_region(self, region, data):
        '''
        Set a given region width provided data.

        Parameters
        ----------

        region : (int,int,int,int)
            an allocated region (x,y,width,height)

        data : numpy array
            data to be copied into given region
        '''
        x, y, width, height = region
        self.data[y:y+height,x:x+width, :] = data


    def get_region(self, width, height):
        '''
        Get a free region of given size and allocate it

        Parameters
        ----------

        width : int
            Width of region to allocate

        height : int
            Height of region to allocate

        Return
        ------
            A newly allocated region as (x,y,width,height) or (-1,-1,0,0)
        '''

        best_height = sys.maxsize
        best_index = -1
        best_width = sys.maxsize
        region = 0, 0, width, height

        for i in range(len(self.nodes)):
            y = self.fit(i, width, height)
            if y >= 0:
                node = self.nodes[i]
                if (y+height < best_height or
                    (y+height == best_height and node[2] < best_width)):
                    best_height = y+height
                    best_index = i
                    best_width = node[2]
                    region = node[0], y, width, height

        if best_index == -1:
            return -1,-1,0,0

        node = region[0], region[1]+height, width
        self.nodes.insert(best_index, node)

        i = best_index+1
        while i < len(self.nodes):
            node = self.nodes[i]
            prev_node = self.nodes[i-1]
            if node[0] < prev_node[0]+prev_node[2]:
                shrink = prev_node[0]+prev_node[2] - node[0]
                x,y,w = self.nodes[i]
                self.nodes[i] = x+shrink, y, w-shrink
                if self.nodes[i][2] <= 0:
                    del self.nodes[i]
                    i -= 1
                else:
                    break
            else:
                break
            i += 1

        self.merge()
        self.used += width*height
        return region



    def fit(self, index, width, height):
        '''
        Test if region (width,height) fit into self.nodes[index]

        Parameters
        ----------

        index : int
            Index of the internal node to be tested

        width : int
            Width or the region to be tested

        height : int
            Height or the region to be tested

        '''

        node = self.nodes[index]
        x,y = node[0], node[1]
        width_left = width

        if x+width > self.width:
            return -1

        i = index
        while width_left > 0:
            node = self.nodes[i]
            y = max(y, node[1])
            if y+height > self.height:
                return -1
            width_left -= node[2]
            i += 1
        return y



    def merge(self):
        '''
        Merge nodes
        '''

        i = 0
        while i < len(self.nodes)-1:
            node = self.nodes[i]
            next_node = self.nodes[i+1]
            if node[1] == next_node[1]:
                self.nodes[i] = node[0], node[1], node[2]+next_node[2]
                del self.nodes[i+1]
            else:
                i += 1


class TextureFont:
    '''
    A texture font gathers a set of glyph relatively to a given font filename
    and size.
    '''

    def __init__(self, atlas, filename, size):
        '''
        Initialize font

        Parameters:
        -----------

        atlas: TextureAtlas
            Texture atlas where glyph texture will be stored

        filename: str
            Font filename

        size : float
            Font size
        '''
        self.atlas = atlas
        self.filename = filename
        self.size = size
        self.glyphs = {}
        face = Face( self.filename )
        face.set_char_size( int(self.size*64))
        self._dirty = False
        metrics = face.size
        self.ascender  = metrics.ascender/64.0
        self.descender = metrics.descender/64.0
        self.height    = metrics.height/64.0
        self.linegap   = self.height - self.ascender + self.descender
        self.depth = atlas.depth
        #set_lcd_filter(FT_LCD_FILTER_LIGHT)


    def __getitem__(self, charcode):
        '''
        x.__getitem__(y) <==> x[y]
        '''
        # print(charcode)
        if charcode not in self.glyphs.keys():
            self.load('%c' % charcode)
        return self.glyphs[charcode]



    def get_texid(self):
        '''
        Get underlying texture identity .
        '''

        if self._dirty:
            self.atlas.upload()
        self._dirty = False
        return self.atlas.texid

    texid = property(get_texid,
                     doc='''Underlying texture identity.''')



    def load(self, charcodes = ''):
        '''
        Build glyphs corresponding to individual characters in charcodes.

        Parameters:
        -----------

        charcodes: [str | unicode]
            Set of characters to be represented
        '''
        face = Face( self.filename )
        pen = Vector(0,0)
        hres = 16*72
        hscale = 1.0/16

        for charcode in charcodes:
            face.set_char_size( int(self.size * 64), 0, hres, 72 )
            matrix = Matrix( int((hscale) * 0x10000), int((0.0) * 0x10000),
                             int((0.0)    * 0x10000), int((1.0) * 0x10000) )
            face.set_transform( matrix, pen )
            if charcode in self.glyphs.keys():
                continue

            self.dirty = True
            flags = FT_LOAD_RENDER | FT_LOAD_FORCE_AUTOHINT
            flags |= FT_LOAD_TARGET_LCD

            face.load_char(charcode, flags )
            bitmap = face.glyph.bitmap
            left   = face.glyph.bitmap_left
            top    = face.glyph.bitmap_top
            width  = face.glyph.bitmap.width
            rows   = face.glyph.bitmap.rows
            pitch  = face.glyph.bitmap.pitch

            x,y,w,h = self.atlas.get_region(width/self.depth+2, rows+2)
            h = int(h)
            w = int(w)
            x = int(x)
            y = int(y)
            if x < 0:
                print ('Missed !')
                continue
            x,y = x+1, y+1
            w,h = w-2, h-2
            data = []
            for i in range(rows):
                data.extend(bitmap.buffer[i*pitch:i*pitch+width])

            data = np.array(data,dtype=np.ubyte).reshape(h,w,3)
            gamma = 1.5
            Z = ((data/255.0)**(gamma))
            data = (Z*255).astype(np.ubyte)
            self.atlas.set_region((x,y,w,h), data)

            # Build glyph
            size   = w,h
            offset = left, top
            advance= face.glyph.advance.x, face.glyph.advance.y

            u0     = (x +     0.0)/float(self.atlas.width)
            v0     = (y +     0.0)/float(self.atlas.height)
            u1     = (x + w - 0.0)/float(self.atlas.width)
            v1     = (y + h - 0.0)/float(self.atlas.height)
            texcoords = (u0,v0,u1,v1)
            glyph = TextureGlyph(charcode, size, offset, advance, texcoords)
            self.glyphs[charcode] = glyph

            # Generate kerning
            for g in self.glyphs.values():
                # 64 * 64 because of 26.6 encoding AND the transform matrix used
                # in texture_font_load_face (hres = 64)
                kerning = face.get_kerning(g.charcode, charcode, mode=FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    glyph.kerning[g.charcode] = kerning.x/(64.0*64.0)
                kerning = face.get_kerning(charcode, g.charcode, mode=FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    g.kerning[charcode] = kerning.x/(64.0*64.0)

            # High resolution advance.x calculation
            # gindex = face.get_char_index( charcode )
            # a = face.get_advance(gindex, FT_LOAD_RENDER | FT_LOAD_TARGET_LCD)/(64*72)
            # glyph.advance = a, glyph.advance[1]


class TextureGlyph:
    '''
    A texture glyph gathers information relative to the size/offset/advance and
    texture coordinates of a single character. It is generally built
    automatically by a TextureFont.
    '''

    def __init__(self, charcode, size, offset, advance, texcoords):
        '''
        Build a new texture glyph

        Parameter:
        ----------

        charcode : char
            Represented character

        size: tuple of 2 ints
            Glyph size in pixels

        offset: tuple of 2 floats
            Glyph offset relatively to anchor point

        advance: tuple of 2 floats
            Glyph advance

        texcoords: tuple of 4 floats
            Texture coordinates of bottom-left and top-right corner
        '''
        self.charcode = charcode
        self.size = size
        self.offset = offset
        self.advance = advance
        self.texcoords = texcoords
        self.kerning = {}


    def get_kerning(self, charcode):
        ''' Get kerning information

        Parameters:
        -----------

        charcode: char
            Character preceding this glyph
        '''
        if charcode in self.kerning.keys():
            return self.kerning[charcode]
        else:
            return 0





class Shader:
    ''' Base shader class. '''

    def __init__(self, vert = None, frag = None, name=''):
        ''' vert, frag and geom take arrays of source strings
            the arrays will be concatenated into one string by OpenGL.'''

        self.uniforms = {}
        self.name = name
        # create the program handle
        self.handle = gl.glCreateProgram()
        # we are not linked yet
        self.linked = False
        # create the vertex shader
        self._build_shader(vert, gl.GL_VERTEX_SHADER)
        # create the fragment shader
        self._build_shader(frag, gl.GL_FRAGMENT_SHADER)
        # the geometry shader will be the same, once pyglet supports the
        # extension self.createShader(frag, GL_GEOMETRY_SHADER_EXT) attempt to
        # link the program
        self._link()

    def _build_shader(self, strings, stype):
        ''' Actual building of the shader '''

        count = len(strings)
        # if we have no source code, ignore this shader
        if count < 1:
            return

        # create the shader handle
        shader = gl.glCreateShader(stype)

        # Upload shader code
        gl.glShaderSource(shader, strings)

        # compile the shader
        gl.glCompileShader(shader)

        # retrieve the compile status
        status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)

        # if compilation failed, print the log
        if not status:
            # display the log
            print (gl.glGetShaderInfoLog(shader))
        else:
            # all is well, so attach the shader to the program
            gl.glAttachShader(self.handle, shader)

    def _link(self):
        ''' Link the program '''

        gl.glLinkProgram(self.handle)
        # retrieve the link status
        temp = ctypes.c_int(0)
        gl.glGetProgramiv(self.handle, gl.GL_LINK_STATUS, ctypes.byref(temp))

        # if linking failed, print the log
        if not temp:
            # retrieve the log length
            gl.glGetProgramiv(self.handle,
                              gl.GL_INFO_LOG_LENGTH, ctypes.byref(temp))
            # create a buffer for the log
            #buffer = ctypes.create_string_buffer(temp.value)
            # retrieve the log text
            log = gl.glGetProgramInfoLog(self.handle) #, temp, None, buffer)
            # print the log to the console
            print (log)
        else:
            # all is well, so we are linked
            self.linked = True

    def bind(self):
        ''' Bind the program, i.e. use it. '''
        gl.glUseProgram(self.handle)

    def unbind(self):
        ''' Unbind whatever program is currently bound - not necessarily this
            program, so this should probably be a class method instead. '''
        gl.glUseProgram(0)

    def uniformf(self, name, *vals):
        ''' Uploads float uniform(s), program must be currently bound. '''

        loc = self.uniforms.get(name,
                                gl.glGetUniformLocation(self.handle,name))
        self.uniforms[name] = loc

        # Check there are 1-4 values
        if len(vals) in range(1, 5):
            # Select the correct function
            { 1 : gl.glUniform1f,
              2 : gl.glUniform2f,
              3 : gl.glUniform3f,
              4 : gl.glUniform4f
              # Retrieve uniform location, and set it
            }[len(vals)](loc, *vals)

    def uniformi(self, name, *vals):
        ''' Upload integer uniform(s), program must be currently bound. '''

        loc = self.uniforms.get(name,
                                gl.glGetUniformLocation(self.handle,name))
        self.uniforms[name] = loc

        # Checks there are 1-4 values
        if len(vals) in range(1, 5):
            # Selects the correct function
            { 1 : gl.glUniform1i,
              2 : gl.glUniform2i,
              3 : gl.glUniform3i,
              4 : gl.glUniform4i
              # Retrieves uniform location, and set it
            }[len(vals)](loc, *vals)


    def uniform_matrixf(self, name, mat):
        ''' Upload uniform matrix, program must be currently bound. '''

        loc = self.uniforms.get(name,
                                gl.glGetUniformLocation(self.handle,name))
        self.uniforms[name] = loc

        # Upload the 4x4 floating point matrix
        gl.glUniformMatrix4fv(loc, 1, False, (ctypes.c_float * 16)(*mat))






# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Subpixel rendering AND positioning using OpenGL and shaders.
'''



vert='''
uniform sampler2D texture;
uniform vec2 pixel;
attribute float modulo;
varying float m;
void main() {
    gl_FrontColor = gl_Color;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    m = modulo;
}
'''

frag='''
uniform sampler2D texture;
uniform vec2 pixel;
varying float m;
void main() {
    float gamma = 1.0;
    vec2 uv      = gl_TexCoord[0].xy;
    vec4 current = texture2D(texture, uv);
    vec4 previous= texture2D(texture, uv+vec2(-1,0)*pixel);
    current  = pow(current,  vec4(1.0/gamma));
    previous = pow(previous, vec4(1.0/gamma));
    float r = current.r;
    float g = current.g;
    float b = current.b;
    float a = current.a;
    if( m <= 0.333 )
    {
        float z = m/0.333;
        r = mix(current.r, previous.b, z);
        g = mix(current.g, current.r,  z);
        b = mix(current.b, current.g,  z);
    }
    else if( m <= 0.666 )
    {
        float z = (m-0.33)/0.333;
        r = mix(previous.b, previous.g, z);
        g = mix(current.r,  previous.b, z);
        b = mix(current.g,  current.r,  z);
    }
   else if( m < 1.0 )
    {
        float z = (m-0.66)/0.334;
        r = mix(previous.g, previous.r, z);
        g = mix(previous.b, previous.g, z);
        b = mix(current.r,  previous.b, z);
    }
   float t = max(max(r,g),b);
   vec4 color = vec4(0.,0.,0., (r+g+b)/2.);
   color = t*color + (1.-t)*vec4(r,g,b, min(min(r,g),b));
   gl_FragColor = vec4( color.rgb, color.a);
}
'''



class Label:
    def __init__(self, text, font, color=(1.0, 1.0, 1.0, 0.0),  x=0, y=0,
                 width=None, height=None, anchor_x='left', anchor_y='baseline'):
        self.text = text
        self.vertices = np.zeros((len(text)*4,3), dtype=np.float32)
        self.indices  = np.zeros((len(text)*6, ), dtype=np.uint)
        self.colors   = np.zeros((len(text)*4,4), dtype=np.float32)
        self.texcoords= np.zeros((len(text)*4,2), dtype=np.float32)
        self.attrib   = np.zeros((len(text)*4,1), dtype=np.float32)
        pen = [x,y]
        prev = None

        for i,charcode in enumerate(text):
            glyph = font[charcode]
            kerning = glyph.get_kerning(prev)
            x0 = pen[0] + glyph.offset[0] + kerning
            dx = x0-int(x0)
            x0 = int(x0)
            y0 = pen[1] + glyph.offset[1]
            x1 = x0 + glyph.size[0]
            y1 = y0 - glyph.size[1]
            u0 = glyph.texcoords[0]
            v0 = glyph.texcoords[1]
            u1 = glyph.texcoords[2]
            v1 = glyph.texcoords[3]

            index     = i*4
            indices   = [index, index+1, index+2, index, index+2, index+3]
            vertices  = [[x0,y0,1],[x0,y1,1],[x1,y1,1], [x1,y0,1]]
            texcoords = [[u0,v0],[u0,v1],[u1,v1], [u1,v0]]
            colors    = [color,]*4

            self.vertices[i*4:i*4+4] = vertices
            self.indices[i*6:i*6+6] = indices
            self.texcoords[i*4:i*4+4] = texcoords
            self.colors[i*4:i*4+4] = colors
            self.attrib[i*4:i*4+4] = dx
            pen[0] = pen[0]+glyph.advance[0]/64.0 + kerning
            pen[1] = pen[1]+glyph.advance[1]/64.0
            prev = charcode

        width = pen[0]-glyph.advance[0]/64.0+glyph.size[0]

        if anchor_y == 'top':
            dy = -round(font.ascender)
        elif anchor_y == 'center':
            dy = +round(-font.height/2-font.descender)
        elif anchor_y == 'bottom':
            dy = -round(font.descender)
        else:
            dy = 0

        if anchor_x == 'right':
            dx = -width/1.0
        elif anchor_x == 'center':
            dx = -width/2.0
        else:
            dx = 0
        self.vertices += (round(dx), round(dy), 0)


    def draw(self):
        gl.glEnable( gl.GL_TEXTURE_2D )
        gl.glDisable( gl.GL_DEPTH_TEST )

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertices)
        gl.glColorPointer(4, gl.GL_FLOAT, 0, self.colors)
        gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, self.texcoords)

        r,g,b = 0,0,0
        gl.glColor( 1, 1, 1, 1 )
        gl.glEnable( gl.GL_BLEND )
        #gl.glBlendFunc( gl.GL_CONSTANT_COLOR_EXT,  gl.GL_ONE_MINUS_SRC_COLOR )
        #gl.glBlendColor(r,g,b,1)
        gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
        gl.glBlendColor( 1, 1, 1, 1 )

        gl.glEnableVertexAttribArray( 1 )
        gl.glVertexAttribPointer( 1, 1, gl.GL_FLOAT, gl.GL_FALSE, 0, self.attrib)
        shader.bind()
        shader.uniformi('texture', 0)
        shader.uniformf('pixel', 1.0/512, 1.0/512)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices),
                          gl.GL_UNSIGNED_INT, self.indices)
        shader.unbind()
        gl.glDisableVertexAttribArray( 1 )
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisable( gl.GL_TEXTURE_2D )
        gl.glDisable( gl.GL_BLEND )


FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")
atlas = TextureAtlas(1000,1000,3)
# atlas.upload()
# font = TextureFont(atlas, FONT, 16)
shader = Shader(vert,frag)
#
# def display(text, x, y):
#     labels = []
#     # x,y = 20,310
#     for i in range(5):
#         labels.append(Label(text=text, font=font, x=x, y=y))
#         x += 10
#         y -= 18
#     gl.glBindTexture( gl.GL_TEXTURE_2D, atlas.texid )
#     for label in labels:
#         label.draw()


if __name__ == '__main__':
    import sys
    import OpenGL.GLUT as glut

    # atlas = TextureAtlas(50,100,3)

    def on_display( ):
        gl.glClearColor(1,1,1,1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glBindTexture( gl.GL_TEXTURE_2D, atlas.texid )
        for label in labels:
            label.draw()

        glut.glutSwapBuffers( )

    def on_reshape( width, height ):
        gl.glViewport( 0, 0, width, height )
        gl.glMatrixMode( gl.GL_PROJECTION )
        gl.glLoadIdentity( )
        gl.glOrtho( 0, width, 0, height, -1, 1 )
        gl.glMatrixMode( gl.GL_MODELVIEW )
        gl.glLoadIdentity( )

    def on_keyboard( key, x, y ):
        if key == '\033':
            sys.exit( )

    glut.glutInit( sys.argv )
    glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH )
    glut.glutCreateWindow( "Freetype OpenGL" )
    glut.glutReshapeWindow( 240, 330 )
    glut.glutDisplayFunc( on_display )
    glut.glutReshapeFunc( on_reshape )
    glut.glutKeyboardFunc( on_keyboard )
    # FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")

    font = TextureFont(atlas, FONT, 16)
    text = u" 你好 Quick Brown Fox Jumps Over The Lazy Dog"
    # text = u"阿斯达稍等无asdasd"
    labels = []
    x,y = 20,310
    for i in range(5):
        labels.append(Label(text=text, font=font, x=x, y=y))
        x += 10
        y -= 18
    atlas.upload()
    # shader = Shader(vert,frag)
    glut.glutMainLoop( )