
import glfw
import time
import traceback
from OpenGL import GL, GLU
from quaking.basic.window import Window
from quaking.basic.engine import Engine

class Basic(object):
    def __init__(self, width, height, title:str='', swap_buffer:bool=False, fps:int=60):
        self.obj_window = Window(width, height, title=title, swap_buffer=swap_buffer)
        self.obj_engine = Engine()
        self.fps = fps

    def frame_rate(self, fps):
        self.fps = fps

    def loop(self, setup=None, draw=None):
        frame_start = 0
        do_setup = False
        while not glfw.window_should_close(self.obj_window.window):
            if self.frame_rate:
                run_time = glfw.get_time()
                time_per_fps = 1 / self.fps
                if run_time - frame_start < time_per_fps:
                    try:
                        time.sleep(time_per_fps - (run_time - frame_start))
                    except Exception:
                        traceback.print_exc()
                frame_start = glfw.get_time()

            # GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            # if self.frame_count <= 1:
            #     # # 初始帧
            #     GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            #     # print("started")
            #     if setup:
            #         setup()
            #         # 获取 setup 之后的背景图 与 宽高
            # else:
            #     if draw != None:
            #         draw()

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
                # GL.glFinish()

            # Poll for and process events
            glfw.poll_events()
            # print(self.frame_count / frame_start)
            # self.frame_count += 1
            # print(self.frame_count)
        glfw.terminate()

