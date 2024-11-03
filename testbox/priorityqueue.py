#!/usr/bin/env python

import heapq
from collections import deque
from typing import Any
import pprint


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item: Any, priority: int) -> None:
        # item is stored with priority first and then the index
        # as the order received
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self) -> Any:
        return heapq.heappop(self._queue)[-1]


if __name__ == "__main__":
    # Unfortunately kafka is a strict one to one message queue and we do not
    # pop off multiple of the stack and set priority.  This seems a downfall
    # if lag is 5 or more with bundle processing. At any point the microservice
    # fails, we lost the consumer topic and payload.
    pq = PriorityQueue()
    pq.push("task1", 9)
    pq.push("task2", 2)
    pq.push("task3", 1)
    pq.push("task4", 1)

    pprint.pp(pq)
    pprint.pp(pq.pop())
    pprint.pp(pq.pop())
    pprint.pp(pq.pop())
    pprint.pp(pq.pop())
