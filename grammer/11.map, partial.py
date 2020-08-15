print("\n*************************************ex1*************************************")
# map
def double(var):
    return var * 2

var = list(map(double, [1, 2, 3]))

print(var)


print("\n*************************************ex2*************************************")

# partial
from functools import partial
def sum(a, b):
    print(a+b*2)

f = partial(sum, b=10)
f(1)


