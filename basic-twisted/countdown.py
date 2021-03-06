
from twisted.internet import reactor

class Countdown:
    def __init__(self, n):

        self.counter = n

    def count(self):
        if self.counter == 0:
            reactor.stop()
        else:
            print(self.counter, '...')
            self.counter -= 1
            reactor.callLater(1, self.count)

from twisted.internet import reactor
reactor.callWhenRunning(Countdown(5).count)
# reactor.callWhenRunning(Countdown(4).count)
print('Start!')
reactor.run()
print('Stop!')
