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

colors = ['#09c', '#90c']
# p1hp, p2dm p1dd
data = [curve(300.0, 30.0, 0.1), curve(300.0, 100.0, 0.5)]
minimum = min(min(data[0][1]), min(data[1][1]))
maximum = max(max(data[0][1]), max(data[1][1]))

tk = Tk()
tk.wm_title('probsim')

width = (maximum - minimum) * 10
height = max(max(data[0][0]), max(data[1][0])) * 1000

lf1 = LabelFrame(master=tk, text="Graph")
lf1.grid(row=0, column=1, padx=20, pady=10, sticky=NS)
canvas = Canvas(master=lf1, width=width + 30, height=height + 30)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Horizontal
for i in range(0, int(height / 10), 5):
    canvas.create_text(width + 20, height - i * 10 + 10, text=i)
    canvas.create_line(10, height - i * 10 + 10, width + 10, height - i * 10 + 10, fill="#ccc")
for i in range(int(minimum), int(maximum), 5):
    canvas.create_text(i * 10 - minimum * 10 + 10, height + 20, text=i)
    canvas.create_line(i * 10 - minimum * 10 + 10, 10, i * 10 - minimum * 10 + 10, height + 10, fill="#ccc")
for i in range(len(data)):
    for j in range(len(data[i][0]) - 1):
        x1 = data[i][1][j] * 10 - minimum * 10 + 10
        y1 = height - data[i][0][j] * 1000 + 10
        x2 = data[i][1][j + 1] * 10 - minimum * 10 + 10
        y2 = height - data[i][0][j + 1] * 1000 + 10
        canvas.create_line(x1, y1, x2, y2, width=3, fill=colors[i])

final = []

r = 0
for i in range(int(min(data[0][1][0], data[1][1][0])), int(min(data[0][1][-1], data[1][1][-1]) + 1)):
    x = i - data[0][1][0]
    y = i - data[1][1][0]
    r += (0 if x < 0 else data[0][0][int(x)]) * (0 if y < 0 else data[1][0][int(y)])

final.append(r)

r = 0
n = 0
for i in range(int(min(data[0][1][0], data[1][1][0])), int(max(data[0][1][-1], data[1][1][-1]) + 1)):
    x = i - data[0][1][0]
    y = i - data[1][1][0]
    n += 0 if 0 > x or x >= len(data[0][0]) else data[0][0][int(x)]
    r += n * (0 if 0 > y or y >= len(data[1][0]) else data[1][0][int(y)])

final.append(r)

r = 0
n = 0
for i in range(int(min(data[0][1][0], data[1][1][0])), int(max(data[0][1][-1], data[1][1][-1]) + 1)):
    x = i - data[0][1][0]
    y = i - data[1][1][0]
    n += 0 if 0 > y or y >= len(data[1][0]) else data[1][0][int(y)]
    r += n * (0 if 0 > x or x >= len(data[0][0]) else data[0][0][int(x)])

final.append(r)

print final
final = [x * 1 / sum(final) for x in final]
tk.update_idletasks()

stretch = canvas.winfo_height()
lf3 = LabelFrame(master=tk, text="Approximate Results")
lf3.grid(row=0, column=3, padx=20, pady=10, sticky=NS)
graph = Canvas(master=lf3, width=190, height=stretch)
graph.grid(row=0, column=0, padx=20, pady=10)
for i in range(11):
    graph.create_line(0, i * (stretch - 40) / 10 + 40, 180, i * (stretch - 40) / 10 + 40, fill="#ccc")
graph.create_rectangle(10, stretch - (stretch - 40) * final[2], 60, stretch, fill=colors[0], outline='')
graph.create_text(35, 20, text="Blue\n" + str(round(final[2] * 100, 2)) + '%')
graph.create_rectangle(70, stretch - (stretch - 40) * final[1], 120, canvas.winfo_height(), fill=colors[1], outline='')
graph.create_text(95, 20, text="Purple\n" + str(round(final[1] * 100, 2)) + '%')
graph.create_rectangle(130, stretch - (stretch - 40) * final[0], 180, canvas.winfo_height(), fill='#999', outline='')
graph.create_text(155, 20, text="Tie\n" + str(round(final[0] * 100, 2)) + '%')


mainloop()
