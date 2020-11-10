
from twisted.internet import reactor

class Countdown:
    def __init__(self, n: int, counters_state: list, current_counter_idx: int):

        self.counter = n
        self.counters_state = counters_state
        self.current_counter_idx = current_counter_idx

    def count(self):
        if self.counter == 0:
            # reactor.stop()
            self.counters_state[self.current_counter_idx] = True
            self.counter_finished()
        else:
            print(self.counter, '...')
            self.counter -= 1
            reactor.callLater(1, self.count)

    def counter_finished(self):
        if len(list(filter(None, self.counters_state))) == len(self.counters_state):
            print('That\'s all')
            reactor.stop()


from twisted.internet import reactor
num_of_counters = 3
conters_state = [False] * num_of_counters
for i in range(num_of_counters):
    reactor.callWhenRunning(Countdown(5, conters_state, i).count)
# reactor.callWhenRunning(Countdown(4).count)
print('Start!')
reactor.run()
print('Stop!')
