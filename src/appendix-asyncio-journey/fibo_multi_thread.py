"""
<출처: https: // hamait.tistory.com / 834[HAMA블로그]>
<output to terminal>

592367971 - Hello world!
1592367974 - Hello world!
10
Executing fib took 0.000272 seconds.
fib(10) = 55
1592367977 - Hello world!
30
Executing fib took 0.399 seconds.
fib(30) = 832040
33
1592367980 - Hello world!
Executing fib took 1.41 seconds.
fib(33) = 3524578
1592367983 - Hello world!
36
1592367986 - Hello world!
1592367989 - Hello world!
Executing fib took 5.76 seconds.
fib(36) = 14930352
"""

import time
from threading import Thread
from fib import timed_fib


def print_hello(t):
    while True:
        print("{} - Hello world!".format(int(time.time())))
        time.sleep(t)


def read_and_process_input():
    while True:
        n = int(input()) # 이때 gil blocking 풀림
        print('fib({}) = {}'.format(n, timed_fib(n)))


def main():
    t = Thread(target=print_hello, args=(3,), daemon=True)
    t.start()
    read_and_process_input()


if __name__ == '__main__':
    main()
