import platform
if platform.system() == 'Windows':
    print("Pollreactor not supported")
else:
    from twisted.internet import pollreactor
    pollreactor.install()

from twisted.internet import reactor
# reactor.run()


def factorial(n):
    if n == 1:
        return n
    else:
        return n * factorial(n-1)

def factorial_(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f
print(1)