import random
import sys
from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        app.background(100, 0, 0)
        app.frame_rate(10)

    def draw():
        app.background(random.randint(50, 100), random.randint(50, 100), random.randint(50, 100))
        # app.size(random.randint(50, 100), random.randint(50, 100))

    app.run( setup, draw )

if __name__ == '__main__':
    main()