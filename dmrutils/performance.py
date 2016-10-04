import time


def clock(func):
    def clocked(*args):
        start = time.time()
        result = func(*args)
        elapsed = time.time() - start
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    