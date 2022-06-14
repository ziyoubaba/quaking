from OpenGL import GL

class EngineConf:
    def __init__(self):
        self.smooth()

    def smooth(self):
        # 开启抗锯齿 way1
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glEnable(GL.GL_POLYGON_SMOOTH)
        # GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)  #
        # way 2
        # GL.glEnable(GL.GL_MULTISAMPLE)

    def no_smooth(self):
        # 关闭抗锯齿功能
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_LINE_SMOOTH)
        GL.glDisable(GL.GL_POINT_SMOOTH)
        GL.glDisable(GL.GL_POLYGON_SMOOTH)

