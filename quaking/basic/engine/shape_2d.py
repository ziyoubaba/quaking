from OpenGL import GL
from functools import wraps
from math import pi, sin, cos, atan2

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


class EngineShape2d():
    def __init__(self):
        self.stroke_weight = 1  # 线条宽度
        self.stroke_color = (0, 0, 0, 255)  # 线条颜色
        self.fill_color = (255, 255, 255, 255)  # 填充颜色

    @wrap_stroke(1)
    def point(self, x, y, z=0, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glBegin(GL.GL_POINTS)
            GL.glVertex3f(x, y, z)
            GL.glEnd()

    @wrap_stroke(1)
    def points(self, points, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glBegin(GL.GL_POINTS)
            for point in points:
                if len(point) == 2:
                    GL.glVertex3f( *point, 0 )
                elif len(point) == 3:
                    GL.glVertex3f( *point )
            GL.glEnd()

    @wrap_stroke(2)
    def line(self, x1, y1, x2, y2, z1=0, z2=0, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(x1, y1, z1)
            GL.glVertex3f(x2, y2, z2)
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
        GL.glVertex3f(x1, y1, 0)
        GL.glVertex3f(x2, y2, 0)
        GL.glVertex3f(x3, y3, 0)
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
        for _index, i in enumerate(arc_points):
            group_points = list(i)
            if _index % 2 == 1:
                group_points.reverse()
            points.extend(group_points)
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

        x = 0
        y = ry
        d1 = ry * ry + rx * rx * (-ry + 0.25)

        arc_points.append(self.get_ellipse_points(xc, yc, x, y))
        last_point = (x, y)
        # //椭圆AC弧段
        while (ry * ry * (x + 1) < rx * rx * (y - 0.5)):
            if (d1 < 0):
                d1 += ry * ry * (2 * x + 3)
            else:
                d1 += ry * ry * (2 * x + 3) + rx * rx * (-2 * y + 2)
                y -= 1
            x += 1
            if last_point[0] == x or last_point[1] == y:
                pass
            else:
                arc_points.append(self.get_ellipse_points(xc, yc, x, y))
                last_point = (x, y)
        # //椭圆CB弧段
        d2 = ry * ry * (x + 0.5) * (x + 0.5) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry
        while (y > 0):
            if (d2 < 0):
                d2 += ry * ry * (2 * x + 2) + rx * rx * (-2 * y + 3)
                x += 1
            else:
                d2 += rx * rx * (-2 * y + 3)
            y -= 1
            if last_point[0] == x or last_point[1] == y:
                pass
            else:
                arc_points.append(self.get_ellipse_points(xc, yc, x, y))
                last_point = (x, y)

        arc_points = zip(*arc_points)
        for _index, i in enumerate(arc_points):
            group_points = list(i)
            if _index % 2 == 0:
                group_points.reverse()
            points.extend(group_points)
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
            GL.glVertex3f(*point, 0)
        GL.glEnd()

    def drawPolygonLine(self, points, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glLineWidth(stroke_weight)
        if stroke_color:
            GL.glColor4ub(*stroke_color)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glBegin(GL.GL_LINE_LOOP)
        for point in points:
            GL.glVertex3f(*point, 0)
        GL.glEnd()

    def drawPolygonFill(self, points, fill_color=None, **kwargs):
        if fill_color:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
            GL.glColor4ub(*fill_color)
            GL.glBegin(GL.GL_POLYGON)
            for point in points:
                GL.glVertex3f(*point, 0)
            GL.glEnd()

    def drawPolygon(self, points, stroke_color=None, stroke_weight=None, fill_color=None):
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

    def drawLineStripLine(self, points, stroke_color=None, stroke_weight=None):
        if stroke_weight:
            GL.glLineWidth(stroke_weight)
        if stroke_color:
            GL.glColor4ub(*stroke_color)
        GL.glBegin(GL.GL_LINE_STRIP)  # 如果绘制整圆，选GL_LINE_LOOP更好
        for point in points:
            GL.glVertex3f(*point, 0)
        GL.glEnd()

    def drawLineStrip(self, line_points, fill_points, stroke_color=None, stroke_weight=None, fill_color=None):
        if not fill_color:
            if stroke_weight:
                # 线框
                self.drawLineStripLine(line_points, stroke_color=stroke_color, stroke_weight=stroke_weight)
        else:
            # 填充与线框
            # 1 填充
            self.drawPolygonFill(fill_points, fill_color=fill_color)
            if stroke_weight:
                # 2 线框
                self.drawLineStripLine(line_points, stroke_color=stroke_color, stroke_weight=stroke_weight)

    @wrap_stroke(2, set_fill=True)
    def circle(self, x, y, diameter, stroke_color=None, stroke_weight=None, fill_color=None):
        radius = int(diameter / 2)
        points = self.circle_points(x, y, radius)
        self.drawPolygon(points, stroke_color=stroke_color, stroke_weight=stroke_weight, fill_color=fill_color)

    def arc_circle(self, x, y, diameter, ts, te):
        """

        :param x:
        :param y:
        :param diameter:
        :param ts:
        :param te:
        :return:
        """
        radius = int(diameter / 2)
        if te < ts:  # 当终止角比起始角还小时，则将终止角加上2π
            te += 2 * pi
        dt = 1 / radius  # 弧度 = 弧长 / 半径，用dt作弧度的改变量
        t = ts  # ts为初始弧度，te为终止弧度
        points = []
        while (t <= te):
            # 按参数方程求出坐标
            xc = x + radius * cos(t)
            yc = y + radius * sin(t)
            t += dt
            points.append((xc, yc))
        return points

    def arc_ellipse(self, x, y, rw, rh, ts, te):
        a = int(rw / 2)
        b = int(rh / 2)

        def eccentric_angle(t):
            return atan2(a * sin(t), b * cos(t))

        dt = 1 / max(a, b)
        t = ts  # ts为初始弧度，te为终止弧度
        points = []
        while (t <= te):
            # 按参数方程求出坐标
            ecc_angle = eccentric_angle(t)
            xc = x + a * cos(ecc_angle)
            yc = y + b * sin(ecc_angle)
            t += dt
            points.append((xc, yc))
        return points

    @wrap_stroke(2, set_fill=True)
    def arc(self, x, y, rw, rh, ts, te, stroke_color=None, stroke_weight=None, fill_color=None, mode=0):
        if rw == rh:
            points = self.arc_circle(x, y, rw, ts, te)
        else:
            points = self.arc_ellipse(x, y, rw, rh, ts, te)
        # print(points)
        if mode == 0:
            # pie filled without line
            line_points = tuple(points)
            points.append((x, y))
            points.insert(0, (x, y))
            fill_points = tuple(points)
        elif mode == 2:
            # pie filled with line
            points.append((x, y))
            points.insert(0, (x, y))
            line_points = tuple(points)
            fill_points = tuple(points)
        elif mode == 3:
            # open
            line_points = fill_points = tuple(points)
        elif mode == 4:
            # CHORD
            points.append(points[0])
            line_points = tuple(points)
            fill_points = tuple(points)
        else:
            line_points = tuple(points)
            points.append((x, y))
            points.insert(0, (x, y))
            fill_points = tuple(points)

        self.drawLineStrip(line_points=line_points, fill_points=fill_points, stroke_color=stroke_color,
                           stroke_weight=stroke_weight, fill_color=fill_color)

    @wrap_stroke(2, set_fill=True)
    def ellipse(self, x, y, a, b, stroke_color=None, stroke_weight=None, fill_color=None):
        rx = int(a / 2)
        ry = int(b / 2)
        points = self.ellipse_points(x, y, rx, ry)
        self.drawPolygon(points, stroke_color=stroke_color, stroke_weight=stroke_weight, fill_color=fill_color)

    def fill(self, r, g, b, a=255):
        self.fill_color = (r, g, b, a)

    def noFill(self):
        self.fill_color = None

    def stroke(self, r, g, b, a=255):
        self.stroke_color = (r, g, b, a)

    def noStroke(self):
        self.stroke_weight = 0

    def strokeWeight(self, w):
        self.stroke_weight = w

    def clear(self):
        # 清除颜色
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

