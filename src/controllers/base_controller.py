from PySide6.QtCore import QObject, Signal


class BaseController(QObject):
    error_occurred = Signal(str)
    loading_started = Signal()
    loading_finished = Signal()

    def __init__(self):
        super().__init__()

    def __connect_signals(self):
        pass
