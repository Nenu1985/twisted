from twisted.internet.defer import Deferred
from twisted.python.failure import Failure


def got_poem(res):
    print('Your poem is served:')
    print(res)

def poem_failed(err):
    print('No poetry for you.')

d = Deferred()

# add a callback/errback pair to the chain
d.addCallbacks(got_poem, poem_failed)

# fire the chain with a normal result
d.callback('This poem is short.')
# d.errback(Failure(Exception('This is the errback')))
print("Finished")
