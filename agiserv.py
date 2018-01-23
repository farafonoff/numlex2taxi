import random
import itertools
from pprint import pprint
import asyncio
from asyncio_extras import threadpool
from panoramisk import fast_agi

import known_operators
import db
import db_maxima_asterisk

def get_devices_for_number(num):
    groups = known_operators.getGroups(db.describeNumber(num))
    devgroups = [db_maxima_asterisk.getDevices(x.group) for x in groups]
    for devs in devgroups:
        random.shuffle(devs)
    devices = itertools.chain(*devgroups)
    channels = [dev.channel for dev in devices]
    return channels

print(known_operators.getGroups(db.describeNumber('9048488073')))
print(known_operators.getGroups(db.describeNumber('89128588538')))
print(known_operators.getGroups(db.describeNumber('+79090561017')))
print(get_devices_for_number('89128588538'))
print(get_devices_for_number('+79090561017'))

loop = asyncio.get_event_loop()

@asyncio.coroutine
def dial_status(request):
    resp = (yield from request.send_command('GET VARIABLE DIALSTATUS'))
    return resp['result'][1]

STATUS_CONTINUE = ['INIT', 'CONGESTION', 'CHANUNAVAIL']

@asyncio.coroutine
async def dialplan(request):
    number = request.headers['agi_extension']
    async with threadpool():
        peers = get_devices_for_number(number)
    for peer in peers:
        pprint(peer)
        await request.send_command('EXEC Dial {}')
        status = dial_status(request)
        pprint(status)
        if ( not (status in STATUS_CONTINUE)):
            break


def main():
    fa_app = fast_agi.Application(loop=loop)
    fa_app.add_route('dial', dialplan)
    coro = asyncio.start_server(fa_app.handler, '0.0.0.0', 4574, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until CTRL+c is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()