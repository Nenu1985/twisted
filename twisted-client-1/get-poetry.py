# This is the Twisted Get Poetry Now! client, version 1.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.

import datetime, errno, optparse, socket

from twisted.internet import main


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 1.0.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-client-1/get-poetry.py 10001 10002 10003

to grab poetry from servers on ports 10001, 10002, and 10003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print(parser.format_help())
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return list(map(parse_address, addresses))


class PoetrySocket(object):

    poem = ''
    
    def __init__(self, task_num, address):
        self.task_num = task_num

        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # conntect with handling an error
        port_is_open = self.sock.connect_ex(address)  # 0 if port is open
        if port_is_open == 0:
            self.sock.setblocking(0)
        else:
            main.CONNECTION_LOST

        # tell the Twisted reactor to monitor this socket for reading
        from twisted.internet import reactor
        reactor.addReader(self)

    def fileno(self):
        try:
            return self.sock.fileno()
        except socket.error:
            return -1

    def connectionLost(self, reason):
        self.sock.close()

        # stop monitoring this socket
        from twisted.internet import reactor
        reactor.removeReader(self)

        # see if there are any poetry sockets left
        for reader in reactor.getReaders():
            if isinstance(reader, PoetrySocket):
                return

        reactor.stop() # no more poetry

    def doRead(self):
        bytes = ''

        while True:
            try:
                bytesread = self.sock.recv(1024).decode()
                if not bytesread:
                    break
                else:
                    bytes += bytesread
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                return main.CONNECTION_LOST

        if not bytes:
            print(f'Task {self.task_num} finished')
            return main.CONNECTION_DONE
        else:
            msg = f'Task {self.task_num}: got {len(bytes)} bytes of poetry from {self.format_addr()}'
            print(msg)

        self.poem += bytes

    def logPrefix(self):
        return 'poetry'

    def format_addr(self):
        host, port = self.address
        return f'{host or "127.0.0.1"}:{port}'


def poetry_main():
    addresses = parse_args()

    start = datetime.datetime.now()

    sockets = [PoetrySocket(i + 1, addr) for i, addr in enumerate(addresses)]

    from twisted.internet import reactor
    reactor.run()

    elapsed = datetime.datetime.now() - start

    for i, sock in enumerate(sockets):
        print(f'Task {i + 1}: {len(sock.poem)} bytes of poetry')

    print(f'Got {len(addresses)} poems in {elapsed}')


if __name__ == '__main__':
    poetry_main()
 