from math import *
from Tkinter import *


def curve(hp, dmg, ddg):
    results = []
    # Rounds needed to hit
    rounds = ceil(hp / dmg)
    # Chance of hit
    chance = 1 - ddg
    i = rounds
    n = 0
    while True:
        o = n
        n = value(i, rounds, chance, ddg)
        results.append(n)
        i += 1
        # Stop if really small or i goes too big
        if (o - n > 0 and n < 0.0001) or i > 100 + rounds:
            break
    rangg = range_(results, 0.9)
    return results


def value(x, rounds, chance, ddg):
    # Hits needed before final hit
    hits = rounds - 1
    # Misses needed before final hit
    misses = x - rounds
    return ddg ** misses * chance ** rounds * ncr(hits + misses, hits)


def ncr(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))


def range_(array, limit):
    start = array.index(max(array))
    d = 0
    while True:
        if sum(array[start - d: start + d + 1]) > limit:
            return [start - d, start + d]
        d += 1
        if d * 2 > len(array):
            break
            # Throws error

data = curve(20.0, 1.0, 0.15)
stretch = [x * 100 for x in data]

tk = Tk()

canvas = Canvas(master=tk, width=1000, height=1000)
canvas.pack()
canvas.create_line(100, 100, 100, 101, fill="red")

for i in range(len(stretch)):
    datum = stretch[i]
    print datum
    canvas.create_line(i * 10, datum * 10 - 1, i * 10, datum * 10 + 1, fill="red")

mainloop()
