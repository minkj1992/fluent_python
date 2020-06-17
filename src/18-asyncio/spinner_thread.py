import itertools
import threading
import time


def spin(msg, done):
    spin_chars = "|/-\\"
    for char in itertools.cycle(spin_chars):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')  # \r: 커서를 그 줄의 맨 앞으로 이동시킴, \r를 통해 터미널에서 작동했던 print 삭제
        if done.wait(.1):  # main에서 set() Event가 들어왔는지 확인하며, timeout 설정만큼 대기한다.
            break
    print(' ' * len(status), end='\r')


def slow_function():
    # pretend waiting a long time for IO bound task
    time.sleep(3)  # pre-emptive scheduling을 위해서 context switching 일어나도록 강제, IO bound 작업
    return 42


def supervisor():
    done = threading.Event()  # for shutdown worker thread
    spinner = threading.Thread(target=spin, args=('thinking', done))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()

    # Set the internal flag to true.
    # Threads that call wait() once the flag is true will not block at all.
    done.set()  # 이게 없으면 worker thread에서 주도권을 main에게 넘겨주지 않는다. (set() -> wait signal
    spinner.join()  # main thread에서 spinner thread 종료를 기다려준다.
    return result


def main():
    result = supervisor()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
