
import datetime


class Log:
    def __init__(self):
        pass

    def log(self, message):
        msg = str(datetime.datetime.now()) + "\t" + message
        print(msg)
