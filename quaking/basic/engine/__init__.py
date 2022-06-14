from quaking.basic.engine.conf import EngineConf
from quaking.basic.engine.shape_2d import EngineShape2d
from quaking.basic.engine.transform import EngineTransform


class Engine(EngineConf, EngineShape2d, EngineTransform):
    def __init__(self):
        EngineConf.__init__(self)
        EngineShape2d.__init__(self)
        EngineTransform.__init__(self)
