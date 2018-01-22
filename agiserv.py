import random
import itertools
from pprint import pprint
import asyncio
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

STATUS_CONTINUE = ['CONGESTION', 'CHANUNAVAIL']

@asyncio.coroutine
def dump_status(request):
    pprint(['DIALSTATUS', (yield from request.send_command('GET VARIABLE DIALSTATUS'))])
    pprint(['HANGUPCAUSE', (yield from request.send_command('GET VARIABLE HANGUPCAUSE'))])

@asyncio.coroutine
def call_waiting(request):
    pprint(['AGI variables:', request.headers])
    pprint((yield from request.send_command('EXEC Dial Local/123@test_busy')))
    yield from dump_status(request)
    pprint((yield from request.send_command('EXEC Dial Local/123@test_congestion')))
    yield from dump_status(request)
    pprint((yield from request.send_command('EXEC Dial Local/123@test_answer')))
    yield from dump_status(request)
    pprint((yield from request.send_command('EXEC Dial Local/123@test_fail')))
    yield from dump_status(request)

def main():
    fa_app = fast_agi.Application(loop=loop)
    fa_app.add_route('call_waiting', call_waiting)
    fa_app.add_route('test', call_waiting)
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