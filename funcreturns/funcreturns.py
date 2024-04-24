#!usr/bin/env python3

import secrets
from dataclasses import dataclass, field
from deprecated import deprecated
from retry import retry

# //////////////////////////////////////////////////////////////////////////////
@deprecated("Using gen_token ain't cool any more", version="1.0.0")
def gen_token():
    return secrets.token_urlsafe(16)

@dataclass(slots=True, kw_only=True)
class Person:
    name: str
    id: str = field(init=False, default_factory=gen_token)

@retry(ZeroDivisionError, delay = 1 ,tries=3, jitter=5)
def do_some_math(value: int) -> float:
    print(f"Running division with {value}")
    rtn = value / 0

result: float = 0.0
try:
    result = do_some_math(10)
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Finished attempt on do_some_math")

def sample(x: int, y: int, z: int):
    return (x+1, y+1, z+1)

(y, z) = sample(1, 2, 3)[1:3]
print("DEBUG: %s and %s" % (y, z))

zzz = Person(name="Jimbo")
print("One-time token: %s" % zzz.id)

# //////////////////////////////////////////////////////////////////////////////
