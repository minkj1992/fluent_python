"""Summary: asyncio와 aiohttp를 사용한 비동기 download 스크립트

Download flags of top 20 countries by population
REST API with <https://www.countryflags.io/:country_code/:style/:size.png>
to get flags of 20 countries png files and download to sub-directory in os.getcwd()

Author: minwook.je
Sample run::
    $ python3 flags_asyncio.py
    BR CD VN NG JP IN MX ID BD KR ET PH PK TR DE EG FR US IR RU
    20 flags downloaded in 2.2633850574 sec

    $ python3 flags_asyncio.py
    CD ET ID MX IR JP KR PK VN DE US PH IN TR FR NG RU BD BR EG
    20 flags downloaded in 2.0549631119 sec
"""

import asyncio

import aiohttp

from flags import BASE_URL, save_flag, show, main_method


async def get_flag(session, country):
    """ request get method to REST API server to get a <country> flag .png file"""

    filestyle = 'flat'
    filesize = '64'
    filetype = 'png'
    url = f'{BASE_URL}/{country}/{filestyle}/{filesize}.{filetype}'
    # download_one의 get_flag(session, country)와 이곳을 번갈아가며 session.get(url)을 모두 요청
    # resp에 모든 client 응답이 추가되면 resp.read()로 넘어간다.
    resp = await session.get(url)

    image = await resp.read()
    return image


async def download_one(loop, country):
    ''''''

    # ClientSession error를 잡기 위해 session을 전달
    # loop = loop를 주어 __aexit__ 처리

    async with aiohttp.ClientSession(loop=loop) as session:
        image = await get_flag(session, country)
    show(country)
    save_flag(image, country.lower(), type='png')
    return country


def download_many(country_list):
    loop = asyncio.get_event_loop()  # new_event_loop은 새로 event loop을 만드는 것
    # 코루틴을 모두 다 생성한다. 함수를 호출하지는 않는다.
    to_do = [download_one(loop, country) for country in
             sorted(country_list)]  # wait() expect a list of futures, not generator
    wait_coro = asyncio.wait(to_do)  # wait for multiple coro, non-blocking, 바로 generator return
    res, _ = loop.run_until_complete(
        wait_coro)  # wait_coro가 스케쥴러에 의해서 완료되기 전까지는 block된다. (heapify를 진행하기 때문에 주어진 리스트 그대로 사용되지는 않고 정렬된다.)
    loop.close()
    return len(res)


if __name__ == '__main__':
    main_method(download_many)
