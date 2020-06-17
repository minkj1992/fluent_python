import asyncio
import itertools


async def spin(msg):
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    print(' ' * len(status), end='\r')


async def slow_function(time):
    await asyncio.sleep(time)
    return 42


async def supervisor():
    # 3.7 version
    # spinner = asyncio.create_task(spin('thinking'))

    # 3.4 ~ 3.6 version
    spinner = asyncio.ensure_future(spin('thinking!'))
    print('spinner object: ', spinner)
    result = await slow_function(3)
    spinner.cancel()
    return result


def main():
    # 3.7 version
    # result = asyncio.run(supervisor())

    # 3.5 ~ 3.6 version
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
