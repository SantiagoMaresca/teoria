from time import time

def count_elapsed_time(f):
    """
    Execute the function and calculate the elapsed time.
    """
    def wrapper(*args):
        # Start counting.
        start_time = time()

        # Take the original function's return value.
        ret = f(*args)

        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        return elapsed_time, ret

    return wrapper