# -*- coding: utf8 -*-

import time

import asyncio
import aiosip
from multidict import CIMultiDict

class PingGW(aiosip.Application):
    def __init__(self, port, *args, **kwargs):
        aiosip.Application.__init__(self, *args, **kwargs)

        self.local_addr=('127.0.0.1', port)
        self.enabled = True

    @asyncio.coroutine
    def handle_options(self, dialog, msg):
        print("handle options::OPTIONS\n", dialog, msg)
        if not self.enabled:
            print(self.local_addr, " disabled")
            return

        headers = CIMultiDict()
        headers['X-Foo'] = 'Bar'
        headers['User-Agent'] = 'kamtester/pinggw/0.1'
        yield dialog.send_reply(200, 'OK', headers=headers)
        self.enabled = False

    @asyncio.coroutine
    def start(self):
        #print(dir(self))
        print("ping gw start")
        self.router.add_route('OPTIONS', self.handle_options)
        yield from self.create_connection(aiosip.UDP, self.local_addr, None, mode='server')

gw = PingGW(port=9922)
print(gw, gw.local_addr)
con = gw.start()

gw2 = PingGW(port=9923)
print(gw2, gw2.local_addr)
con2 = gw2.start()

#loop = asyncio.get_event_loop()
loop = gw.loop
loop.run_until_complete(con)
loop.run_until_complete(con2)
loop.run_forever()

