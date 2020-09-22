import time
from time import monotonic

def timeout(time_out):
    '''
    Retries a function or method until it returns True or timeout is reached.
    Timeout in seconds

    Use as a decorator when defining the the function:
    @timeout(5)
    def fun():
        print('hi')
        if random.random() > 0.8:
            return True
    '''
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            t=monotonic()
            rv = f(*args, **kwargs) # first attempt
            while time_out > monotonic()-t:
                if rv:
                    return True
                rv = f(*args, **kwargs) # Try again
            print('TIMED OUT:',f)
            return False # timed out
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator
