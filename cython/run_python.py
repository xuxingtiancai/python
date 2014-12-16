from math import sin

x = 0
i = 0
while i < 3000000:
    x = sin(x + 1)
    i += 1

print x
