from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint


class Server(Protocol):
    def connectionMade(self):
        print('New connection')
        self.transport.write('Hello from server'.encode('utf-8'))

    def dataReceived(self, data: bytes):
        self.transport.write(data)


class ServerFactory(ServFactory):
    def buildProtocol(self, address):
        return Server()


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2000)
    endpoint.listen(ServerFactory())
    reactor.run()
