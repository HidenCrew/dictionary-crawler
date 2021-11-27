import time

DEBUG = False


def log(string):
    if DEBUG:
        print(string)


def get_time_str() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def get_output_base() -> str:
    return "output/"


def read_clean_words() -> list:
    return [line for line in open("input_words.txt").read().splitlines() if line.strip()]
