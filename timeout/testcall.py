from timeout import timeout,TimeoutError
import time
import os
import errno

# Timeout a long running function with the default expiry of 10 seconds.
@timeout()
def long_running_function1():
    ...

# Timeout after 5 seconds
@timeout(5)
def long_running_function2():
    print("Running function2 ...")
    time.sleep(10)

# Timeout after 30 seconds, with the error "Connection timed out"
@timeout(30, os.strerror(errno.ETIMEDOUT))
def long_running_function3():
    ...

if __name__ == "__main__":
    try:
        long_running_function1()
        long_running_function2()
        long_running_function3()
    except TimeoutError as err:
        print("TimeoutError: ", err)
    except Exception as err:
        print("Oops", type(err).__name__,"with", err)
    finally:
        print("Completed")
    
