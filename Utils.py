import time

DEBUG = False


def log(str):
    if DEBUG:
        print(str)


def getTimeStr() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def getOutputBase() -> str:
    return "output/"
