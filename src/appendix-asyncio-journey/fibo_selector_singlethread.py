"""
Selector와 while loop(event loop)을 활용하여
sys.stdin event 발생 시 context switching이 일어나게 동작
"""

import sys
import selectors
from time import time
from fib import timed_fib


def process_input(stream):
    # stream is <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>
    text = stream.readline()
    n = int(text.strip())
    print('[fileboj: {}]--> fib({}) = {}'.format(id(stream), n, timed_fib(n))) # [fileboj: 140591049069912]--> fib(5) = 5


def print_hello():
    print("{} - Hello world!".format(int(time())))


def main():
    selector = selectors.DefaultSelector() # Default is SelectSelector
    selector.register(sys.stdin, selectors.EVENT_READ)
    last_hello = 0  # Setting to 0 means the timer will start right away
    while True:
        for event, mask in selector.select(.1): # .1초 동안 block 시키고 register 시킨 event가 발생했는지 확인
            process_input(event.fileobj)
        if time() - last_hello > 3:
            last_hello = time()
            print_hello()


if __name__ == '__main__':
    main()
