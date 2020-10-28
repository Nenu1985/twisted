
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
class Countdown:
    def __init__(self, n):

        self.counter = n

    def count(self):

        print(self.counter, '...')
        self.counter -= 1
        return self.counter


from twisted.internet import reactor
c1 = Countdown(5)
c1_loop = LoopingCall(c1.count)

c1_loop.start(1.0)

# while True:
#     print(c1.counter)


# reactor.callWhenRunning(Countdown(4).count)
print('Start!')
reactor.run()
print('Stop!')
