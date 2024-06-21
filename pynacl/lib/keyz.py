from dataclasses import dataclass
from datetime import datetime
from time import sleep
from nacl.encoding import Base64Encoder
from nacl.utils import random
from retry import retry
import atexit
import signal

@dataclass
class keyz:
    id: str
    public_key: bytes()

    def __post_init__(self):
        ###########################################################
        atexit.register(self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
        ###########################################################

    def produce(self) -> str:
        now = datetime.now()
        print(f"[{now}] Generating from {self.id}")
        sleep(1)
        return Base64Encoder().encode(self.public_key).decode('utf-8')

    def breakdown(self) -> int:
        return len(self.id)

    @retry(delay=60, tries=10, jitter=60)
    def randomizer(self) -> str:
        bstring = random(size=32)
        mystring = Base64Encoder().encode(bstring).decode('utf-8')
        if mystring.startswith('H') or mystring.startswith('G'):
            print("Ok we good.")
        else:
            print(f"{datetime.now()} - This is not what I want - {mystring}")
            raise RuntimeError("The hell with this!")
        return mystring

    def shutdown(self) -> None:
        print("Closing connections to keyz")


if __name__ == "__main__":
    print("Not to be called here. See ya!")
