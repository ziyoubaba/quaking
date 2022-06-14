from quaking.basic.engine.conf import EngineConf
from quaking.basic.engine.shape_2d import EngineShape2d


class Engine(EngineConf, EngineShape2d, ):
    def __init__(self):
        EngineConf.__init__(self)
        EngineShape2d.__init__(self)
