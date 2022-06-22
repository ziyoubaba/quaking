from OpenGL import GL
from OpenGL.GL import shaders

class EngineShader():
    #compiling shaders
    # vertexshader = shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER)
    # fragmentshader = shaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER)
    # shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    # GL.glUseProgram(shaderProgram)
    #problem
    # shader_projection = GL.glGetUniformLocation(shaderProgram, "projection")
    # projection = glm.ortho(0, 640, 640, 0)
    # GL.glUniformMatrix4fv(shader_projection, 1, GL.GL_FALSE, glm.value_ptr(projection))

    def __init__(self):
        pass
