import atexit

def byebye():
    print("The great escape from most wanted.")

def reddington() -> str:
    return "Raymond"

atexit.register(byebye)
