import glfw, time

class Keyboard:
    # 鼠标按键
    # 键盘
    KEYUP = 265
    KEYDOWN = 264
    KEYLEFT = 263
    KEYRIGHT = 262
    KEYALT = 342
    KEYCTL = 341
    KEYLSHIFT = 340
    KEYRSHIFT = 344
    KEYTAB = 258
    KEYCAPS = 280
    KEYESC = 256
    KEYBACKSPACE = 259
    KEYRETURN = 257
    KEYENTER = 257
    KEYDELETE = 261

    def __init__(self, quaking):
        self.quaking = quaking
        # 键盘变量
        self.key = None
        self.key_pressed = False
        self.key_code = None  #

    def key_callback(self, window, key_code, _, status, extra):
        print("keyboard ", key_code, status)
        self.key_code = key_code
        if status == 1:
            self.key_pressed = True
        elif status == 2:
            self.key_pressed = True
        else:
            self.key_pressed = False
        if self.key_pressed:
            self.keyPressed(key_code=key_code, status=status)
            if status == 2:
                self.keyTyped(key_code=key_code)
        else:
            self.keyReleased(key_code=key_code)

    def char_callback(self, window, ascii_code):
        # print("char  ", ascii_code)
        self.key = chr(ascii_code)
        # print(self.key)

    def keyTyped(self, key_code):
        print("typed key:", key_code, chr(key_code))
        pass

    def keyPressed(self, key_code, status):
        """
        :param key_code: keycode
        :param status: 1:press 2:hold
        :return:
        """
        print("pressed key:", key_code, chr(key_code), status)
        pass

    def keyReleased(self, key_code):
        """
        :param key_code: keycode
        :return:
        """
        print("released key:", key_code, chr(key_code))
        pass