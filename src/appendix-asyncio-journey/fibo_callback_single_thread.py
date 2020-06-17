import sys
import selectors
from time import time
from bisect import insort
from collections import namedtuple, deque
from fib import timed_fib

Timer = namedtuple('Timer', ('timestamp', 'handler'))


class EventLoop:
    """
    Implements a callback based single-threaded event loop

    단점: 이러한 스타일이 특히 오류 처리가 추가되면 매우 빠르게 콜백 지옥이 형성된다.
    """

    def __init__(self, *tasks):
        self._running = False
        self._stdin_handlers = list()  # This is for callback functions without timer
        self._timers = deque([]) # (callback, time)
        self._selector = selectors.DefaultSelector()
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def run_forever(self, time_out=0):
        self._running = True
        while self._running:
            # first check for without timer callback (IO input)
            for key, mask in self._selector.select(time_out):
                line = key.fileobj.readline().strip()
                for callback in self._stdin_handlers:
                    print(callback)
                    callback(line)

            # Handle timer events: consumer
            while self._timers and self._timers[0].timestamp < time():
                handler = self._timers.popleft().handler
                handler()

    def add_stdin_handler(self, callback):
        self._stdin_handlers.append(callback)

    def add_timer(self, wait_time, callback):
        timer = Timer(timestamp=time() + wait_time, handler=callback)
        insort(self._timers, timer)

    def stop(self):
        self._running = False

def on_stdin_input(line):
    if line == 'exit':
        loop.stop()
        return
    try:
        n = int(line)
        print("fib({}) = {}".format(n, timed_fib(n)))
    except ValueError:
        print(f"invalid literal for int() with '{line}'")

# print Hello world, Before add Timer callback: inf producer
def print_hello():
    print("{} - Hello world!".format(int(time())))
    loop.add_timer(3, print_hello)


def main():
    global loop
    loop = EventLoop()
    loop.add_stdin_handler(on_stdin_input) # add callback without timer
    loop.add_timer(0, print_hello) # add callback with timer
    loop.run_forever()


if __name__ == '__main__':
    main()
