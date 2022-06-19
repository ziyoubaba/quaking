from OpenGL import GL
from functools import wraps
from math import pi, sin, cos, atan2
from PIL import Image

from OpenGL.GL import *
import glm

class EngineImage():
    def __init__(self):
        pass

    def image(self, obj_image, x, y, width, height):
        """

        :param obj_image:
        :param x:
        :param y:
        :return:
        """
        img_format = GL.GL_RGB if obj_image.mode == "RGB" else GL.GL_RGBA
        # 1 create a texture
        texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, img_format, obj_image.size[0], obj_image.size[1], 0, img_format,
                        GL.GL_UNSIGNED_BYTE, obj_image.tobytes())
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f( 0.0, 0.0 ); GL.glVertex3f( x, y, 0 )
        GL.glTexCoord2f( 1.0, 0.0 ); GL.glVertex3f( x+width, y, 0 )
        GL.glTexCoord2f( 1.0, 1.0 ); GL.glVertex3f( x+width, y+height, 0 )
        GL.glTexCoord2f( 0.0, 1.0 ); GL.glVertex3f( x, y+height, 0 )
        GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)

    def load_image(self, image_file):
        # load the image using Pillow
        obj_image = Image.open(image_file)
        return obj_image

    def image_light0(self, obj_image, x, y, width, height):
        img_format = GL.GL_RGB if obj_image.mode == "RGB" else GL.GL_RGBA

        # unsigned int hdrFBO;
        hdrFBO = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, hdrFBO)
        # unsigned int colorBuffers[2];
        colorBuffers = GL.glGenTextures(2, )
        img_w, img_h = obj_image.size
        for i in range(2):
            GL.glBindTexture(GL.GL_TEXTURE_2D, colorBuffers[i])
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA16F, img_w, img_h, 0, GL.GL_RGBA, GL.GL_FLOAT, None)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            # // attach texture to framebuffer
            GL.glFramebufferTexture2D(
                GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0 + i, GL.GL_TEXTURE_2D, colorBuffers[i], 0
            )
        attachments = [ GL.GL_COLOR_ATTACHMENT0, GL.GL_COLOR_ATTACHMENT1 ]
        GL.glDrawBuffers(2, attachments)

        # unsigned int pingpongFBO[2];
        # unsigned int pingpongColorbuffers[2];
        pingpongFBO = GL.glGenFramebuffers(2)
        pingpongColorbuffers = GL.glGenTextures(2)
        for i in range(2):
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, pingpongFBO[i])
            GL.glBindTexture(GL.GL_TEXTURE_2D, pingpongColorbuffers[i])
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA16F, img_w, img_h, 0, GL.GL_RGBA, GL.GL_FLOAT, None)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE) # we clamp to the edge as the blur filter would otherwise sample repeated texture values!
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, pingpongColorbuffers[i], 0)
            # // also check if framebuffers are complete (no need for depth buffer)
            # if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE)
            #     std.cout << "Framebuffer not complete!" << std.endl;

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, img_format, obj_image.size[0], obj_image.size[1], 0, img_format,
                        GL.GL_UNSIGNED_BYTE, obj_image.tobytes())

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, hdrFBO)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f( 0.0, 0.0 ); GL.glVertex3f( x, y, 0 )
        GL.glTexCoord2f( 1.0, 0.0 ); GL.glVertex3f( x+width, y, 0 )
        GL.glTexCoord2f( 1.0, 1.0 ); GL.glVertex3f( x+width, y+height, 0 )
        GL.glTexCoord2f( 0.0, 1.0 ); GL.glVertex3f( x, y+height, 0 )
        GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)

        # // lighting info
        # // -------------
        # // positions
        # std.vector<glm.vec3> lightPositions;
        # lightPositions = []
        # lightPositions.append(GL.GL_FLOAT_VEC3( 0.0, 0.5,  1.5))
        # lightPositions.append(GL.GL_FLOAT_VEC3(-4.0, 0.5, -3.0))
        # lightPositions.append(GL.GL_FLOAT_VEC3( 3.0, 0.5,  1.0))
        # lightPositions.append(GL.GL_FLOAT_VEC3(-.8,  2.4, -1.0))
        # # // colors
        # # std.vector<glm.vec3> lightColors;
        # lightColors = []
        # lightColors.append(GL.GL_FLOAT_VEC3(5.0,   5.0,  5.0))
        # lightColors.append(GL.GL_FLOAT_VEC3(10.0,  0.0,  0.0))
        # lightColors.append(GL.GL_FLOAT_VEC3(0.0,   0.0,  15.0))
        # lightColors.append(GL.GL_FLOAT_VEC3(0.0,   5.0,  0.0))

    def image_light(self, obj_image, x, y, width, height):
        img_format = GL.GL_RGB if obj_image.mode == "RGB" else GL.GL_RGBA
        SCR_WIDTH, SCR_HEIGHT = obj_image.size
        glEnable(GL_DEPTH_TEST)
        hdrFBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, hdrFBO)
        # // create 2 floating point color buffers (1 for normal rendering, other for brightness threshold values)
        colorBuffers = glGenTextures(2)
        for i in range(2):
            glBindTexture(GL_TEXTURE_2D, colorBuffers[i])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16F, SCR_WIDTH, SCR_HEIGHT, 0, GL_RGBA, GL_FLOAT, None)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  # we clamp to the edge as the blur filter would otherwise sample repeated texture values!
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            # // attach texture to framebuffer
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + i, GL_TEXTURE_2D, colorBuffers[i], 0)
        # // create and attach depth buffer (renderbuffer)
        rboDepth = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rboDepth)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, SCR_WIDTH, SCR_HEIGHT)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rboDepth)
        # // tell OpenGL which color attachments we'll use (of this framebuffer) for rendering
        attachments = [ GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1 ]
        glDrawBuffers(2, attachments)
        # // finally check if framebuffer is complete
        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
            print("Framebuffer not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # // ping-pong-framebuffer for blurring
        # unsigned int pingpongFBO[2];
        # unsigned int pingpongColorbuffers[2];
        pingpongFBO = glGenFramebuffers(2, )
        pingpongColorbuffers = glGenTextures(2, )
        for i in range(2):
            glBindFramebuffer(GL_FRAMEBUFFER, pingpongFBO[i]);
            glBindTexture(GL_TEXTURE_2D, pingpongColorbuffers[i]);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16F, SCR_WIDTH, SCR_HEIGHT, 0, GL_RGBA, GL_FLOAT, None);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); # we clamp to the edge as the blur filter would otherwise sample repeated texture values!
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, pingpongColorbuffers[i], 0);
            # // also check if framebuffers are complete (no need for depth buffer)
            if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
                print("Framebuffer not complete!" )

        # // lighting info
        # // -------------
        # // positions
        # std.vector<glm.vec3> lightPositions;
        lightPositions = []
        lightPositions.append(glm.vec3(0.0, 0.5, 1.5))
        lightPositions.append(glm.vec3(-4.0, 0.5, -3.0))
        lightPositions.append(glm.vec3(3.0, 0.5, 1.0))
        lightPositions.append(glm.vec3(-.8, 2.4, -1.0))
        # // colors
        lightColors = []
        # std.vector<glm.vec3> lightColors;
        lightColors.append(glm.vec3(5.0, 5.0, 5.0))
        lightColors.append(glm.vec3(10.0, 0.0, 0.0))
        lightColors.append(glm.vec3(0.0, 0.0, 15.0))
        lightColors.append(glm.vec3(0.0, 5.0, 0.0))


        # // shader configuration
        # // --------------------
        # shader.use();
        # shader.setInt("diffuseTexture", 0);
        # shaderBlur.use();
        # shaderBlur.setInt("image", 0);
        # shaderBloomFinal.use();
        # shaderBloomFinal.setInt("scene", 0);
        # shaderBloomFinal.setInt("bloomBlur", 1);

