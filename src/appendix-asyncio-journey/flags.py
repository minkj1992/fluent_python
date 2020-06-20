"""Download flags of top 20 countries by population
REST API with <https://www.countryflags.io/:country_code/:style/:size.png> to get flags of 20 countries png files and download to sub-directory in os.getcwd()
Sample run::
    $ python3 flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 flags downloaded in 20.00 sec
"""

import os
import time

import requests

POP20_CC = ('KR IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = "https://www.countryflags.io"

DEST_DIR = os.path.join(os.getcwd(), "downloads/flags")


def get_flag(country):
    """ request get method to REST API server to get a <country> flag .png file"""

    filestyle = 'flat'
    filesize = '64'
    filetype = 'png'
    url = f'{BASE_URL}/{country}/{filestyle}/{filesize}.{filetype}'
    resp = requests.get(url)
    return resp.content


def show(serialized):
    """ To show progress status to console(flush True)"""

    print(serialized, end=' ', flush=True)  # print문에 flush()강제 가능하다.


def save_flag(img, filename):
    """ Download img to DEST_DIR"""

    path = os.path.join(DEST_DIR, filename + '.png')  # TODO: /이 없어야 join이 제대로 동작한다.
    with open(path, 'wb') as fp:
        fp.write(img)


def download_many(country_list):
    """Download flags in Synchronous way with for-loop"""

    for country in sorted(country_list):
        image = get_flag(country)
        show(country)
        save_flag(image, country.lower())
    return len(country_list)  # TODO: 중간에 다운로드 실패할 경우


def main(download_many):
    """ Log process time and delegate the process to download method()"""
    start_time = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - start_time
    msg = '\n flags downloaded in {:.2f} sec'
    print(msg.format(count, elapsed))


def make_dir():
    """존재하더라도 error 내지않으며, 존재하지 않는다면 디렉토리들을 생성해준다."""
    os.makedirs(DEST_DIR, exist_ok=True)


if __name__ == '__main__':
    make_dir()
    main(download_many)
