import argparse
import sys
import os
import atexit

libdir :str = os.path.realpath(os.path.dirname(__file__) + '/../lib')
print(f"Path to LIB: {libdir}")
sys.path.append(libdir)

from keyz import keyz
from blacklist import reddington

def arg_run(value: str) -> None:
    byte_message = value.encode()
    mykey = keyz('job12341234q234124', byte_message)
    asdf = mykey.produce()
    print(f"b64[{mykey.breakdown()}]: {asdf}")
    try:
        print(f"random: {mykey.randomizer()}")
    except Exception as excp:
        print(f"[{type(excp).__name__}] - Out of luck, we ran out of randoms.", excp)

def basic_test() -> None:
    mykey = keyz('job12341234q234123', b'asdfasdfasdfqwerqwerqwerqwer')
    asdf = mykey.produce()
    print(f"b64[{mykey.breakdown()}]: {asdf}")

def byebye():
    print("That's all folks")

if __name__ == "__main__":
    atexit.register(byebye)
    print(f"Blacklist - {reddington()}")
    #basic_test()
    # arg testing
    parser = argparse.ArgumentParser()
    #parser.add_argument('-d', '--dmp', default=None)
    parser.add_argument('message', nargs='?', type=str,
                        default='Hellothisisalongerstringtoproduceinto')
    args = parser.parse_args()
    #print(f"args.dmp: {args.dmp}")
    print(f"args.message: {args.message}")
    arg_run(args.message)
