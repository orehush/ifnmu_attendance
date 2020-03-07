import string
import random


def generate_code():
    return ''.join([random.choice(string.digits + 'QWRZGS') for _ in range(4)])
