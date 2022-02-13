"""
Setup for example monkeypatch
"""

from json import JSONDecodeError
import requests
import numpy
import datetime

#//////////////////////////////////////////////////////////////////////////////////////////////////
def power(a, b):
    return a ** b

def caller_to_power(a, b):
    print("Sending %g ^ %g" % (a , b))
    return ("Result: %g" % power(a, b))

def fc_shipment(start=datetime.date(2022,1, 1), end=datetime.date.today()):
    return numpy.busday_count(start, end)

def add_business_days(start=datetime.date(2022,1,28), numbus=1):
    return numpy.busday_offset(start, numbus + 1, roll='forward')

#//////////////////////////////////////////////////////////////////////////////////////////////////
class FooBarBaz:
    def get_elapsed_time(self, url):
        r = requests.get(url)
        return r.elapsed.total_seconds()

#//////////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__": # pragma: no cover
    print(caller_to_power(2,8))
    foo = FooBarBaz()
    try:
        print("Time spent: ", foo.get_elapsed_time(url="https://google.com"))
    except JSONDecodeError as excp:
        raise("ERROR: Json decode error - %s" % str(excp))
    finally:
        print("Request completed")

    start = datetime.date(2022,1, 28)
    end   = datetime.date.today()
    print("Number of business days since new year 2022: %g" % fc_shipment())
    print("Expected delivery date when sent on %s: %s" % (start, add_business_days(start, 2)))
    print("Expected after 2 work weeks after %s: %s" % (start, add_business_days(start, 10)))
    print("Number of days past due since %s: %g" % (start, fc_shipment(start, end)))
    print("Adding 30 days after %s has %s business days" % (
        start, 
        fc_shipment(start, start + datetime.timedelta(days=30))
        ))