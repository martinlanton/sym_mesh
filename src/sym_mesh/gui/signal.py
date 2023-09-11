import logging

logger = logging.getLogger(__name__)


class Signal(object):
    def __init__(self):
        super(Signal, self).__init__()
        self.triggers = []

    def connect(self, func):
        """Connect the emission of that signal to the selected function.

        :param func:
        :return:
        """
        self.triggers.append(func)

    def emit(self, arg):
        for func in self.triggers:
            func(arg)
