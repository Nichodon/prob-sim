from math import *
from Tkinter import *
import ttk


# p1hp, p2dm p1dd

tk = Tk()
tk.wm_title('probsim')

inputs = [500, 100, 0.5, 0.3, 0.9, 300, 200, 0.7, 0.7, 0.1]


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


def validate(action, value_if_allowed, text):
    if action == '1':
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        return False
    return True


def update():
    global inputs, canvas, graph, lf1, lf3

    try:
        inputs = [float(x.get()) for x in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]]
        if inputs[2] > 1 or inputs[7] > 1:
            return
    except ValueError:
        pass

    try:
        canvas.pack_forget()
        graph.pack_forget()
        lf1.grid_forget()
        lf3.grid_forget()
    except NameError:
        pass

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
    try:
        d1 = inputs[6] * (1 - max(inputs[3] - inputs[9], 0))
        d2 = inputs[1] * (1 - max(inputs[8] - inputs[4], 0))
        data = [curve(inputs[0], d1, inputs[2]), curve(inputs[5], d2, inputs[7])]
    except ValueError:
        return

    minimum = min(min(data[0][1]), min(data[1][1]))
    maximum = max(max(data[0][1]), max(data[1][1]))

    width = (maximum - minimum) * 10
    height = max(max(data[0][0]), max(data[1][0])) * 1000

    lf1 = LabelFrame(master=tk, text='Graph')
    lf1.grid(row=0, column=1, pady=10, sticky=NS)
    canvas = Canvas(master=lf1, width=width + 30, height=height + 30)
    canvas.pack(padx=10, pady=10, expand=True)

    # Horizontal
    for i in range(0, int(height / 10), 5):
        canvas.create_text(width + 20, height - i * 10 + 10, text=i)
        canvas.create_line(10, height - i * 10 + 10, width + 10, height - i * 10 + 10, fill="#ccc")
    for i in range(int(minimum), int(maximum), 5):
        canvas.create_text(i * 10 - minimum * 10 + 10, height + 20, text=i)
        canvas.create_line(i * 10 - minimum * 10 + 10, 10, i * 10 - minimum * 10 + 10, height + 10, fill="#ccc")
    for i in range(len(data)):
        x1 = data[i][1][0] * 10 - minimum * 10 + 10
        y1 = height - data[i][0][0] * 1000 + 10
        canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, fill=colors[i], outline='')
        for j in range(len(data[i][0]) - 1):
            x1 = data[i][1][j] * 10 - minimum * 10 + 10
            y1 = height - data[i][0][j] * 1000 + 10
            x2 = data[i][1][j + 1] * 10 - minimum * 10 + 10
            y2 = height - data[i][0][j + 1] * 1000 + 10
            canvas.create_line(x1, y1, x2, y2, width=3, fill=colors[i])
        x1 = data[i][1][-1] * 10 - minimum * 10 + 10
        y1 = height - data[i][0][-1] * 1000 + 10
        canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, fill=colors[i], outline='')

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

    final = [x * 1 / sum(final) for x in final]
    tk.update_idletasks()

    stretch = max(canvas.winfo_height(), 350)
    lf3 = LabelFrame(master=tk, text="Approximate Chance of Win")
    lf3.grid(row=0, column=2, padx=10, pady=10, sticky=NS)
    graph = Canvas(master=lf3, width=190, height=stretch)
    graph.pack(padx=20, pady=10, expand=True)
    for i in range(11):
        graph.create_line(0, i * (stretch - 40) / 10 + 40, 190, i * (stretch - 40) / 10 + 40, fill="#ccc")
    graph.create_rectangle(10, stretch - (stretch - 40) * final[2], 60, stretch, fill=colors[0], outline='')
    graph.create_text(35, 20, text="Blue\n" + str(round(final[2] * 100, 2)) + '%')
    graph.create_rectangle(70, stretch - (stretch - 40) * final[1], 120, stretch, fill=colors[1], outline='')
    graph.create_text(95, 20, text="Purple\n" + str(round(final[1] * 100, 2)) + '%')
    graph.create_rectangle(130, stretch - (stretch - 40) * final[0], 180, stretch, fill='#999', outline='')
    graph.create_text(155, 20, text="Tie\n" + str(round(final[0] * 100, 2)) + '%')

colors = ['#09c', '#90c']
command = tk.register(validate), '%d', '%P', '%S'

lf2 = LabelFrame(master=tk, text="Customization")
lf2.grid(row=0, column=0, padx=10, pady=10, sticky=NS)
f1 = Frame(master=lf2)
f1.pack(expand=True)
s1 = ttk.Separator(master=f1)
s1.grid(row=6, column=0, columnspan=2, sticky=EW, padx=10)
s2 = ttk.Separator(master=f1)
s2.grid(row=12, column=0, columnspan=2, sticky=EW, padx=10)
b1 = Button(master=f1, text="Update", command=update, padx=10, pady=5, relief=GROOVE)
b1.grid(row=13, column=0, sticky=W, padx=10, pady=10)

e1 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e1.grid(row=1, column=1, padx=10, pady=10)
e2 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e2.grid(row=2, column=1, padx=10, pady=10)
e3 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e3.grid(row=3, column=1, padx=10, pady=10)
e4 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e4.grid(row=4, column=1, padx=10, pady=10)
e5 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e5.grid(row=5, column=1, padx=10, pady=10)
l1 = Label(master=f1, text="Health Points", foreground=colors[0])
l1.grid(row=1, column=0, padx=10, pady=10, sticky=W)
l2 = Label(master=f1, text="Attack Damage", foreground=colors[0])
l2.grid(row=2, column=0, padx=10, pady=10, sticky=W)
l3 = Label(master=f1, text="Dodge Percent", foreground=colors[0])
l3.grid(row=3, column=0, padx=10, pady=10, sticky=W)
l4 = Label(master=f1, text="Armor Percent", foreground=colors[0])
l4.grid(row=4, column=0, padx=10, pady=10, sticky=W)
l5 = Label(master=f1, text="Pierce Percent", foreground=colors[0])
l5.grid(row=5, column=0, padx=10, pady=10, sticky=W)

e6 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e6.grid(row=7, column=1, padx=10, pady=10)
e7 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e7.grid(row=8, column=1, padx=10, pady=10)
e8 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e8.grid(row=9, column=1, padx=10, pady=10)
e9 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e9.grid(row=10, column=1, padx=10, pady=10)
e10 = Entry(master=f1, vcmd=command, highlightbackground='#ccc', highlightthickness=1, bd=0)
e10.grid(row=11, column=1, padx=10, pady=10)
l6 = Label(master=f1, text="Health Points", foreground=colors[1])
l6.grid(row=7, column=0, padx=10, pady=10, sticky=W)
l7 = Label(master=f1, text="Attack Damage", foreground=colors[1])
l7.grid(row=8, column=0, padx=10, pady=10, sticky=W)
l8 = Label(master=f1, text="Dodge Percent", foreground=colors[1])
l8.grid(row=9, column=0, padx=10, pady=10, sticky=W)
l9 = Label(master=f1, text="Armor Percent", foreground=colors[1])
l9.grid(row=10, column=0, padx=10, pady=10, sticky=W)
l10 = Label(master=f1, text="Pierce Percent", foreground=colors[1])
l10.grid(row=11, column=0, padx=10, pady=10, sticky=W)

for entry in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]:
    entry.insert(END, inputs[[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10].index(entry)])
    entry.config(validate='key')

update()
mainloop()
