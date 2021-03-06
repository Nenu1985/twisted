# This is the asynchronous Get Poetry Now! client.

import datetime, errno, optparse, select, socket


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, asynchronous edition.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python async-client/get-poetry.py 10001 10002 10003

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


def get_poetry(sockets):
    """Download poety from all the given sockets."""

    poems = dict.fromkeys(sockets, '') # socket -> accumulated poem

    # socket -> task numbers
    sock2task = dict([(s, i + 1) for i, s in enumerate(sockets)])

    sockets = list(sockets) # make a copy

    # we go around this loop until we've gotten all the poetry
    # from all the sockets. This is the 'reactor loop'.

    while sockets:
        # this select call blocks until one or more of the
        # sockets is ready for read I/O
        rlist, _, _ = select.select(sockets, [], [])

        # rlist is the list of sockets with data ready to read

        for sock in rlist:
            data = ''

            while True:
                try:
                    new_data = sock.recv(1024).decode()
                except socket.error as e:
                    if e.args[0] == errno.EWOULDBLOCK:
                        # this error code means we would have
                        # blocked if the socket was blocking.
                        # instead we skip to the next socket
                        # print(sock, e)
                        break
                    raise
                else:
                    if not new_data:
                        break
                    else:
                        data += new_data

            # Each execution of this inner loop corresponds to
            # working on one asynchronous task in Figure 3 here:
            # http://krondo.com/?p=1209#figure3

            task_num = sock2task[sock]

            if not data:
                sockets.remove(sock)
                sock.close()
                print(f'Task {task_num} finished')
            else:
                addr_fmt = format_address(sock.getpeername())
                msg = f'Task {task_num}: got {len(data)} bytes of poetry from {addr_fmt}'
                print(msg)

            poems[sock] += data

    return poems


def connect(address):
    """Connect to the given server and return a non-blocking socket."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.setblocking(0)
    return sock


def format_address(address):
    host, port = address
    return f'{host}:{port}'


def main():
    addresses = parse_args()

    start = datetime.datetime.now()

    sockets = list(map(connect, addresses))

    poems = get_poetry(sockets)

    elapsed = datetime.datetime.now() - start

    for i, sock in enumerate(sockets):
        print(f'Task {i + 1}: {len(poems[sock])} bytes of poetry')

    print(f'Got {len(addresses)} poems in {elapsed}')


if __name__ == '__main__':
    main()
