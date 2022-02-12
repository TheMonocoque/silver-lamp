"""
Setup for example monkeypatch
"""

from json import JSONDecodeError
import requests

def power(a, b):
    return a ** b

def caller_to_power(a, b):
    print("Sending %g ^ %g" % (a , b))
    return ("Result: %g" % power(a, b))

#//////////////////////////////////////////////////////////////////////////////////////////////////
class FooBarBaz:
    def get_elapsed_time(self, url):
        """Takes a URL, and returns the JSON."""
        try:
            r = requests.get(url)
            print("JSON: %s" % r.json())
        except JSONDecodeError as excp:
            print("ERROR: Json decode error - %s" % str(excp))
        finally:
            print("Request completed")
        return r.elapsed.total_seconds()
#//////////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__": # pragma: no cover
    print(caller_to_power(2,8))
    foo = FooBarBaz()
    print(foo.get_elapsed_time(url="https://google.com"))