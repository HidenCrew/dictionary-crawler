import time

DEBUG = False


def log(str):
    if DEBUG:
        print(str)


def get_time_str() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def get_output_base() -> str:
    return "output/"
