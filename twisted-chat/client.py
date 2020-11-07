from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint


class Client(Protocol):
    def __init__(self) -> None:
        reactor.callInThread(self.send_data)

    def dataReceived(self, data: bytes):
        data = data.decode('utf-8')
        print(data)

    def send_data(self):
        while True:
            self.transport.write(input().encode('utf-8'))


class ClientFactory(ClFactory):
    def buildProtocol(self, address):
        return Client()


if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 2000)
    endpoint.connect(ClientFactory())
    reactor.run()
