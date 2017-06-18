from math import *
from Tkinter import *


def curve(hp, dmg, ddg):
    results = []
    numbers = []
    rounds = ceil(hp / dmg)
    chance = 1 - ddg
    x = rounds
    n = 0
    results.append(0)
    numbers.append(x - 1)
    while True:
        o = n
        hits = rounds - 1
        misses = x - rounds
        n = ddg ** misses * chance ** rounds * ncr(hits + misses, hits)
        results.append(n)
        numbers.append(x)
        x += 1
        if (o - n > 0 and n < 0.0001) or x > 100 + rounds:
            break
    return [results, numbers]


def ncr(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))

'''
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
'''

data = curve(300.0, 10.0, 0.5)
stretch = [x * 100 for x in data[0]]
print stretch

print data[1]

tk = Tk()

width = len(stretch) * 10 + 30
height = max(stretch) * 10 + 30
canvas = Canvas(master=tk, width=width, height=height)
canvas.pack()

for i in range(0, 101, 5):
    if height - i * 10 - 20 < 10:
        break
    canvas.create_text(width - 20, height - i * 10 - 20, text=i)
    canvas.create_line(10, height - i * 10 - 20, width - 30, height - i * 10 - 20, fill="#ccc")
for i in range(len(data[1]))[0::5]:
    canvas.create_text(i * 10 + 10, height - 10, text=str(int(data[1][i])))
    canvas.create_line(i * 10 + 10, 10, i * 10 + 10, height - 20, fill="#ccc")
for i in range(len(stretch) - 1):
    datum = stretch[i]
    later = stretch[i + 1]
    canvas.create_line(i * 10 + 10, height - datum * 10 - 20, i * 10 + 20, height - later * 10 - 20, fill="#90c", width=3)

mainloop()
