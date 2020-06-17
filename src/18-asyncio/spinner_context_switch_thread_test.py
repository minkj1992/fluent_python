import threading
import time

"""
<context switching test>

결론: python에서 thread context switching은 runnable하지 않은 상태일 때만 일어나며, sleep()같이 thread blcok을 시키지 않는다면, 
하나의 쓰레드가 계속해서 주도권을 가지고 실행된다. (즉 context switching이 일어나지 않는다.)
"""

def spin(msg, done):
    while True:
        status = "Worker Thread is Running"
        print(status)
        if done.wait(.1):
            break


def slow_function():
    while True:
        print("Main Thread is Running")
        time.sleep(.1)


def supervisor():
    done = threading.Event()
    spinner = threading.Thread(target=spin, args=('thinking', done))
    print('spinner object:', spinner)
    spinner.start()
    slow_function()
    spinner.join()
    return

def main():
    result = supervisor()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
