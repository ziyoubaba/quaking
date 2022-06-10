from OpenGL import GL, GLU
from functools import partial, wraps

def wrap_stroke(shape=0, set_fill=False):
    def _func(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            kwargs.update(dict(zip(fn.__code__.co_varnames[1:], args)))
            stroke_color = kwargs.get("stroke_color", None)
            stroke_weight = kwargs.get("stroke_weight", None)

            if set_fill:
                fill_color = kwargs.get("fill_color", None)
                if not fill_color and self.fill_color:
                    kwargs["fill_color"] = self.fill_color
            # print(kwargs)
            # 设置线条颜色
            if stroke_color:
                # print(stroke_color)
                GL.glColor4ub(*stroke_color)
            elif self.stroke_color:
                GL.glColor4ub(*self.stroke_color)
                kwargs['stroke_color'] = self.stroke_color
            # 设置线条宽度
            if stroke_weight is not None:
                pass
            elif self.stroke_weight is not None:
                stroke_weight = self.stroke_weight
            if stroke_weight < 0:
                stroke_weight = 0
            kwargs['stroke_weight'] = stroke_weight
            if stroke_weight:
                if shape == 1:
                    GL.glPointSize(stroke_weight)
                elif shape == 2:
                    GL.glLineWidth(stroke_weight)
            ret = fn(self, **kwargs)
            return ret
        return wrapper
    return _func


class Engine():
    def __init__(self):
        self.background_color = (235, 235, 235, 255)
        self.stroke_weight = 1  # 线条宽度
        self.stroke_color = (0, 0, 0, 255)  # 线条颜色
        self.fill_color = None  # 填充颜色

    @wrap_stroke(1)
    def point(self, x, y, z=0, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glBegin(GL.GL_POINTS)
            GL.glVertex2f(x, y)
            GL.glEnd()

    @wrap_stroke(2)
    def line(self, x1, y1, x2, y2, z1=0, z2=0, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(x1, y1)
            GL.glVertex2f(x2, y2)
            GL.glEnd()

    def drawQuad(self, x1, y1, x2, y2, x3, y3, x4, y4, z1=0, z2=0, z3=0, z4=0):
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3f(x1, y1, z1)
        GL.glVertex3f(x2, y2, z2)
        GL.glVertex3f(x3, y3, z3)
        GL.glVertex3f(x4, y4, z4)
        GL.glEnd()

    def drawRect(self, x1, y1, x2, y2):
        """
        :param x1: 左上x坐标
        :param y1: 左上y坐标
        :param x2: 右下x坐标
        :param y2: 右下y坐标
        :return:
        """
        GL.glRectf(x1, y1, x2, y2)

    def drawTriangle(self, x1, y1, x2, y2, x3, y3):
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex2f(x1, y1)
        GL.glVertex2f(x2, y2)
        GL.glVertex2f(x3, y3)
        GL.glEnd()

    def get_circle_points(self, xc, yc, x, y):
        # todo 优化迭代器的使用
        yield [
            (xc + y, yc + x), (xc + x, yc + y), (xc - x, yc + y), (xc - y, yc + x),
            (xc - y, yc - x), (xc - x, yc - y), (xc + x, yc - y), (xc + y, yc - x),
        ]

    def circle_points(self, xc, yc, radius):
        x = 0
        y = radius
        p = 3 - 2 * radius

        points = []
        arc_points = []
        last_point = None  # (250, 400), (263, 399)
        while (x <= y):
            # print("last", last_point)
            if last_point:
                if last_point[0] == x or last_point[1] == y:
                    line_as_last_point = True
                else:
                    line_as_last_point = False
            else:
                line_as_last_point = False
            if line_as_last_point == False:
                for i in self.get_circle_points(xc, yc, x, y):
                    arc_points.append(i)
            last_point = (x, y)
            if p < 0:
                p += 4 * x + 6
            else:
                p += 4 * (x - y) + 10
                y -= 1
            x += 1
        arc_points = zip(*arc_points)
        _index = 0
        for i in arc_points:
            group_points = list(i)
            if _index % 2 == 1:
                group_points.reverse()
            points.extend(group_points)
            _index += 1
        # print( points )
        return points

    def get_ellipse_points(self, xc, yc, x, y):
        # return [(xc + x, yc + y), (xc - x, yc + y),  (xc - x, yc - y), (xc + x, yc - y)  ]
        return [(xc + x, yc + y), (xc - x, yc + y), (xc - x, yc - y), (xc + x, yc - y)]

    def ellipse_points(self, xc, yc, rx, ry):
        """
        :param xc:
        :param yc:
        :param rx:
        :param ry:
        :return:
        """
        points = []
        arc_points = []
        # (250, 400), (263, 399)

        a = rx
        b = ry
        # double x,y,d1,d2,a,b;
        x = 0
        y = b
        d1 = b * b + a * a * (-b + 0.25)

        arc_points.append(self.get_ellipse_points(xc, yc, x, y))
        last_point = (x, y)
        # //椭圆AC弧段
        while (b * b * (x + 1) < a * a * (y - 0.5)):
            if (d1 < 0):
                d1 += b * b * (2 * x + 3)
            else:
                d1 += b * b * (2 * x + 3) + a * a * (-2 * y + 2)
                y -= 1
            x += 1
            if last_point[0] == x or last_point[1] == y:
                pass
            else:
                arc_points.append(self.get_ellipse_points(xc, yc, x, y))
                last_point = (x, y)
        # //椭圆CB弧段
        d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
        while (y > 0):
            if (d2 < 0):
                d2 += b * b * (2 * x + 2) + a * a * (-2 * y + 3)
                x += 1
            else:
                d2 += a * a * (-2 * y + 3)
            y -= 1
            if last_point[0] == x or last_point[1] == y:
                pass
            else:
                arc_points.append(self.get_ellipse_points(xc, yc, x, y))
                last_point = (x, y)

        arc_points = zip(*arc_points)
        _index = 0
        for i in arc_points:
            group_points = list(i)
            if _index % 2 == 0:
                group_points.reverse()
            points.extend(group_points)
            _index += 1
        return points

    @wrap_stroke(2, set_fill=True)
    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4, stroke_color=None, stroke_weight=None, fill_color=None):
        if not fill_color:
            if stroke_weight:
                # 线框
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawQuad(x1, y1, x2, y2, x3, y3, x4, y4)
            else:
                return
        else:
            # 填充与线框
            # 1 填充
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*fill_color)
            self.drawQuad(x1, y1, x2, y2, x3, y3, x4, y4)
            if stroke_weight:
                # 2 线框
                if stroke_color:
                    GL.glColor4ub(*stroke_color)
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawQuad(x1, y1, x2, y2, x3, y3, x4, y4)

    @wrap_stroke(2, set_fill=True)
    def triangle(self, x1, y1, x2, y2, x3, y3, stroke_color=None, stroke_weight=None, fill_color=None):
        if not fill_color:
            if stroke_weight:
                # 线框
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawTriangle(x1, y1, x2, y2, x3, y3)
            else:
                return
        else:
            # 填充与线框
            # 1 填充
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*fill_color)
            self.drawTriangle(x1, y1, x2, y2, x3, y3)
            if stroke_weight:
                # 2 线框
                if stroke_color:
                    GL.glColor4ub(*stroke_color)
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawTriangle(x1, y1, x2, y2, x3, y3)

    @wrap_stroke(2, set_fill=True)
    def rect(self, x, y, w, h, stroke_color=None, stroke_weight=None, fill_color=None):
        # print(stroke_weight, stroke_color, fill_color)
        x2 = x + w
        y2 = y + h
        if not fill_color:
            if stroke_weight:
                # 线框
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawRect(x, y, x2, y2)
        else:
            # 填充与线框
            # 1 填充
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*fill_color)
            self.drawRect(x, y, x2, y2)
            if stroke_weight:
                # 2 线框
                if stroke_color:
                    GL.glColor4ub(*stroke_color)
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                self.drawRect(x, y, x2, y2)

    @wrap_stroke(1, set_fill=False)
    def drawPoints(self, points, stroke_color=None, stroke_weight=None):
        GL.glBegin(GL.GL_POINTS)
        for point in points:
            GL.glVertex2f(*point)
        GL.glEnd()

    def drawPolygonLine(self, points, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glLineWidth(stroke_weight)
        if stroke_color:
            GL.glColor4ub(*self.stroke_color)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)  #
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        # GL.glEnable(GL.GL_LINE_STIPPLE)
        # GL.glEnable(GL.GL_BLEND)
        # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_DST_ALPHA)
        # GL.glEnable(GL.GL_POLYGON_SMOOTH)
        # GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)
        GL.glBegin(GL.GL_LINE_LOOP)
        for point in points:
            GL.glVertex2f(*point)
        GL.glEnd()

    @wrap_stroke(2, set_fill=False)
    def drawPolygon_remove(self, points, stroke_color=None, stroke_weight=None, fill_color=None):

        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glPolygonMode(GL.GL_BACK, GL.GL_FILL)

        GL.glBegin(GL.GL_LINE_LOOP)
        for point in points:
            GL.glVertex2f(*point)
        GL.glVertex2f(*points[0])
        points.reverse()
        for point in points:
            GL.glVertex2f(*point)
        GL.glEnd()

    def drawPolygonFill(self, points, fill_color=None, **kwargs):
        if fill_color:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*fill_color)
            GL.glBegin(GL.GL_POLYGON)
            for point in points:
                GL.glVertex2f(*point)
            GL.glEnd()

    @wrap_stroke(2, set_fill=True)
    def circle(self, x, y, diameter, stroke_color=None, stroke_weight=None, fill_color=None):
        radius = int(diameter / 2)
        points = self.circle_points(x, y, radius)

        if not fill_color:
            if stroke_weight:
                # 线框
                self.drawPolygonLine(points, stroke_color=stroke_color, stroke_weight=stroke_weight)
        else:
            # 填充与线框
            # 1 填充
            self.drawPolygonFill(points, fill_color=fill_color)
            if stroke_weight:
                # 2 线框
                self.drawPolygonLine(points, stroke_color=stroke_color, stroke_weight=stroke_weight)

    def arc(self):
        pass

    @wrap_stroke(2, set_fill=True)
    def ellipse(self, x, y, a, b, stroke_color=None, stroke_weight=None, fill_color=None):
        rx = int(a / 2)
        ry = int(b / 2)
        points = self.ellipse_points(x, y, rx, ry)
        if not fill_color:
            if stroke_weight:
                # 线框
                self.drawPolygonLine(points, stroke_color=stroke_color, stroke_weight=stroke_weight)
        else:
            # 填充与线框
            # 1 填充
            self.drawPolygonFill(points, fill_color=fill_color)
            if stroke_weight:
                # 2 线框
                self.drawPolygonLine(points, stroke_color=stroke_color, stroke_weight=stroke_weight)
