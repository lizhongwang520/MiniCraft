import time
import threading


class Thread(object):

    def __init__(self, func, *args):
        threading.Thread(target=func, args=args).start()
