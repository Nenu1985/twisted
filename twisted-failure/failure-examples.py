# This code illustrates a few aspects of Failures.
# Generally, Twisted makes Failures for us.

from twisted.python.failure import Failure

class RhymeSchemeViolation(Exception): pass


print('Just making an exception:')
print()

e = RhymeSchemeViolation('ha ha ha')

failure = Failure(e)

# Note this failure doesn't include any traceback info
print('first failure::: ', failure)

print()
print()

print('Catching an exception:')
print()

def analyze_poem(poem):
    raise RhymeSchemeViolation('ga ga ga')

try:
    analyze_poem("""\
Roses are red.
Violets are violet.
That's why they're called Violets.
Duh.
""")
except Exception as ex:
    failure2 = Failure(ex) # = failure2 = Failure()


# This failure saved both the exception and the traceback
print(f'failure:::', failure2)
