from functools import wraps
def memo(fn):
    @wraps(fn)
    def wrapper(*args):
        result = wrapper.cache.get(args)
        if result is None:
            result = fn(*args)
            wrapper.cache[args] = result
        return result
    wrapper.cache = {}
    return wrapper
