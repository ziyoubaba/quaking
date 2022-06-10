from OpenGL import GL, GLU


class ColorSetting:
    def __init__(self, quaking):
        # todo 支持图片
        self.quaking = quaking
        self.background_color = None

    def background(self, r, g, b, a=255):
        self.background_color = (r, g, b, a)
        # print(self.background_color)
        if self.background_color[-1] == 255:
            # 不透明
            r, g, b, a = self.background_color
            GL.glClearColor(r / 255, g / 255, b / 255, a / 255)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        elif self.background_color[-1] == 0:
            # 完全透明 不画
            pass
        elif self.background_color:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthFunc(GL.GL_ALWAYS)
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*self.background_color)
            self.quaking.obj_engine.drawQuad(0, 0, self.quaking.width, 0, self.quaking.width, self.quaking.height,
                                                   0, self.quaking.height, 1, 1, 1, 1)
            GL.glDisable(GL.GL_DEPTH_TEST)
