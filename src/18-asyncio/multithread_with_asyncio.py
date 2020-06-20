'''
총 2가지 쓰레드에서 (Main Thread 와 work Thread) work Thread를 비동기 통신을 진행을 테스트하여
worker Thread의 non blocking 여부를 확인한다.

Author: minwook.je
Sample run::
    $ python3 multithread_with_asyncio.py

    sleep(1)
    RU US DE PK ID JP IN MX ET EG FR
    <<Interrupt Main Thread from worker_thread>>
    NG TR PH VN BD IR BR CD KR
    20 flags downloaded in 1.5023951530 sec
'''

import threading
import asyncio
import aiohttp
import time
from flags import BASE_URL, save_flag, show, main_method


async def get_flag(session, country):
    """ request get method to REST API server to get a <country> flag .png file"""

    filestyle = 'flat'
    filesize = '64'
    filetype = 'png'
    url = f'{BASE_URL}/{country}/{filestyle}/{filesize}.{filetype}'
    resp = await session.get(url)

    image = await resp.read()
    return image


async def download_one(loop, country):
    async with aiohttp.ClientSession(loop=loop) as session:
        image = await get_flag(session, country)
    show(country)
    save_flag(image, country.lower(), type='png')
    return country


def download_many(country_list):
    loop = asyncio.new_event_loop()
    to_do = [download_one(loop, country) for country in
             sorted(country_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


def interrupt_printer():
    print("sleep(1)")
    time.sleep(1)
    print()
    print("<<Interrupt Main Thread from worker_thread>>")


if __name__ == '__main__':
    # worker_thread = threading.Thread(target=main_method, args=(download_many,))
    worker_thread = threading.Thread(target=interrupt_printer)
    worker_thread.start()
    main_method(download_many)
    worker_thread.join()
