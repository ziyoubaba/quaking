import glfw, time

class Mouse:
    # 鼠标按键
    MOUSE_LEFT = 0  # 左键
    MOUSE_RIGHT = 1  # 右
    MOUSE_MID = 2  # 中间

    # 鼠标箭头形状
    MOUSE_ARROW = 0
    MOUSE_IBEAM = 1
    MOUSE_CROSSHAIR = 2
    MOUSE_HAND = 3
    MOUSE_HRESIZE = 4
    MOUSE_VRESIZE = 5
    MOUSE_IMAGE = 6

    def __init__(self, quaking):
        self.quaking = quaking
        self.mouseX, self.mouseY = self.initMousePos(quaking.obj_window.window)
        self.pmouseX, self.pmouseY = self.mouseX, self.mouseY
        self.mouse_pressed = False
        self.mouse_button = None
        self.mouse_dragged = False
        self.mouse_click_delay = 300  # ms
        self.mouse_events = {}

    def initMousePos(self, window):
        x, y = glfw.get_cursor_pos(window)
        return x, y

    def cursor(self, shape=None, img=None, x=0, y=0):
        # glfw.set_input_mode(self.window, glfw.HAND_CURSOR, glfw.CURSOR_NORMAL)
        if not shape:
            shape = 0
        if shape == self.MOUSE_ARROW:
            cursor = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        elif shape == self.MOUSE_IBEAM:
            cursor = glfw.create_standard_cursor(glfw.IBEAM_CURSOR)
        elif shape == self.MOUSE_CROSSHAIR:
            cursor = glfw.create_standard_cursor(glfw.CROSSHAIR_CURSOR)
        elif shape == self.MOUSE_HAND:
            cursor = glfw.create_standard_cursor(glfw.HAND_CURSOR)
        elif shape == self.MOUSE_HRESIZE:
            cursor = glfw.create_standard_cursor(glfw.HRESIZE_CURSOR)
        elif shape == self.MOUSE_VRESIZE:
            cursor = glfw.create_standard_cursor(glfw.VRESIZE_CURSOR)
        elif shape == self.MOUSE_IMAGE:
            if img:
                # todo 创建图片型指针
                pass
            cursor = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        else:
            cursor = glfw.create_standard_cursor(glfw.ARROW_CURSOR)
        glfw.set_cursor(self.quaking.obj_window.window, cursor)
        glfw.set_input_mode(self.quaking.obj_window.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def noCursor(self):
        glfw.set_input_mode(self.quaking.obj_window.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)

    # callback
    def mouse_position_callback(self, window, posx, posy):
        # print("鼠标位置：", posx, posy, self.mouse_dragged)
        self.pmouseX, self.pmouseY = self.mouseX, self.mouseY
        self.mouseX, self.mouseY = posx, posy
        self.mouse_dragged = self.mouse_pressed  # 是否拖拽
        self.mouseMoved()
        if self.mouse_dragged:
            self.mouseDragged()

    def mouse_button_callback(self, window, btn_id, status, extra):
        # print( "鼠标点击", btn_id, status, extra )
        # glfw.MOUSE_BUTTON_LEFT
        if status == 1:
            # 点击操作
            self.mouse_pressed = True
            self.mouse_button = btn_id
            self.mousePressed()
            self.mouse_events[(btn_id, status)] = (time.time() * 1000)
        else:
            # 松开操作
            self.mouse_pressed = False
            self.mouse_button = None
            # 判断clicked - 点击然后松开代表的是clicked事件
            if self.mouse_events:
                event_tsp = self.mouse_events.pop((btn_id, 1), None)
                if event_tsp:
                    if time.time() * 1000 - event_tsp < self.mouse_click_delay:
                        self.mouseClicked(btn_id)
            self.mouseReleased()

    def mouse_scroll_callback(self, window, *scroll):
        # print( "鼠标滚动", scroll,  )
        self.mouseWheel()

    # 自定义事件
    def mouseClicked(self, btn_id=None):
        # print("点击了", btn_id)
        pass
        # if btn_id == self.MouseLeft:
        #     self.stroke_weight = 3

    def mouseDragged(self, *args, **kwargs):
        # print("拖拽", *args, **kwargs)
        pass

    def mouseMoved(self, *args, **kwargs):
        # print("移动", *args, **kwargs)
        pass

    def mousePressed(self, *args, **kwargs):
        # print("长按", *args, **kwargs)
        pass

    def mouseReleased(self, *args, **kwargs):
        # print("松开", *args, **kwargs)
        pass

    def mouseWheel(self, *args, **kwargs):
        # print("滚动", *args, **kwargs)
        pass