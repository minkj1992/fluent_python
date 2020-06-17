import sys
import types
import selectors
from time import time
from bisect import insort
from functools import partial
from collections import deque
from collections import namedtuple
from fib import timed_fib

Timer = namedtuple('Timer', ['timestamp', 'handler'])


class sleep_for_seconds:
    """
    Yield an object of this type from a coroutine to have it "sleep"
    for the given number of seconds.
    """

    def __init__(self, wait_time):
        self._wait_time = wait_time  # TODO: why?


class EventLoop:
    """
    Implements a simplified coroutine-based event-loop as a demonstration.
    Very similar to the "Trampoline" example in PEP 342
    with exception handling taken out for simplicity, and selectors added to handle file IO
    """

    def __init__(self, *tasks):
        self._running = False
        self._selector = selectors.DefaultSelector()  # SelectSelector

        # Queue of functions scheduled to run
        self._tasks = deque(tasks)

        # (coroutine, stack) pair of tasks waiting for input from stdin
        # without timer
        self._tasks_waiting_on_stdin = []

        # List of (time_to_run, task) pairs, in sorted order
        # with timer
        self._timers = []

        # Register for polling stdin for input to read
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def resume_task(self, coroutine, value=None, stack=()):
        result = coroutine.send(value)
        if isinstance(result, types.GeneratorType):
            self.schedule(result, None, (coroutine, stack))
        elif isinstance(result, sleep_for_seconds):
            self.schedule(coroutine, None, stack, time() + result._wait_time)
        elif result is sys.stdin:
            self._tasks_waiting_on_stdin.append((coroutine, stack))
        elif stack:
            self.schedule(stack[0], result, stack[1])

    def schedule(self, coroutine, value=None, stack=(), when=None):
        """
        Schedule a coroutine task to be run, with value to be sent to it.
        And stack containing the coroutines that are waiting for the value yielded
        by this coroutine.
        :param coroutine: coroutine
        :param value: to be sent to coroutine
        :param stack: contains the coroutines
        :param when: time to yield
        :var task:
            - 함수형 프로그래밍의 Currying 기법(여러개의 인자를 받는 함수를 나머지 인자를 받는 함수로 변환하는 메커니즘)
            - 여기서는 함수를 실행하지 않으면서 인자로 func를 넣어주기 위해 사용
            - partial()에 의해 callable 타입들이 생성되어 들어있다.
        :return: None
        """
        task = partial(self.resume_task, coroutine, value, stack)

        if when:
            insort(self._timers, Timer(timestamp=when, handler=task))
        else:
            self._tasks.append(task)

    def stop(self):
        self._running = False

    def do_on_next_tick(self, func, *args, **kwargs):
        self._tasks.appendleft(partial(func, *args, **kwargs))

    def run_foever(self):
        self._running = True
        while self._running:
            # First check for available IO input
            for key, mask in self._selector.select(0):
                line = key.fileobj.readline().strip()
                for task, stack in self._tasks_waiting_on_stdin:
                    self.schedule(task, line, stack)
                self._tasks_waiting_on_stdin.clear()

            # Next, run the next task
            if self._tasks:
                task = self._tasks.popleft()
                task()

            # Finally, run time scheduled tasks
            # bisect로 insort해야하니 deque가 아닌 list로 작성
            while self._timers and self._timers[0].timestamp < time():
                task = self._timers[0].handler
                del self._timers[0]
                task()

        self._running = False  # TODO: why?


def print_every(message, interval):
    """
    Coroutine task to repeatedly print the message at the given interval
    (in seconds)
    """
    while True:
        print("{} - {}".format(int(time()), message))
        yield sleep_for_seconds(interval)


def read_input(loop):
    """
    Coroutine task to repeatedly read new lines of input from stdin, treat
    the input as a number n, and calculate and display fib(n).
    """
    while True:
        line = yield sys.stdin
        if line == 'exit':
            loop.do_on_next_tick(loop.stop)
            continue
        n = int(line)
        print("fib({}) = {}".format(n, timed_fib(n)))


def main():
    loop = EventLoop()
    hello_task = print_every('Hello world!', 3)
    fib_task = read_input(loop) # 여기서 block 될까?
    loop.schedule(hello_task)
    loop.schedule(fib_task)
    loop.run_foever()


if __name__ == '__main__':
    main()
