
import glfw
import time
import traceback
from OpenGL import GL, GLU
from quaking.basic.window import Window
from quaking.basic.engine import Engine

class Basic(object):
    def __init__(self, width, height, title:str='', swap_buffer:bool=False, fps:int=60, obj_window=None):
        self.swap_buffer = swap_buffer
        self.title = title
        if not obj_window:
            self.obj_window = Window(width, height, title=title, swap_buffer=swap_buffer)
        else:
            self.obj_window = obj_window
        self.obj_engine = Engine()
        self.fps = fps
        self.frame_count = 0
        self.refresh = False

    def frame_rate(self, fps):
        self.fps = fps

    def loop(self, setup=None, draw=None):
        frame_start = 0
        do_setup = False
        while not glfw.window_should_close(self.obj_window.window):
            if self.fps:
                run_time = glfw.get_time()
                time_per_fps = 1 / self.fps
                if run_time - frame_start < time_per_fps:
                    try:
                        time.sleep(time_per_fps - (run_time - frame_start))
                    except Exception:
                        traceback.print_exc()
                frame_start = glfw.get_time()

            # GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            # Swap front and back buffers
            if setup and not do_setup:
                setup()
                do_setup = True
            elif draw:
                draw()

            if self.obj_window.swap_buffer:
                glfw.swap_buffers(self.obj_window.window)
            else:
                GL.glFlush()
                # self.obj_window.read_gl_pixels()

            # Poll for and process events
            glfw.poll_events()
            self.frame_count += 1
            # 是否重启
            if self.refresh:
                do_setup = False
                self.refresh = False

        glfw.terminate()

