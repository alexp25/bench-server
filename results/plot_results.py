import matplotlib.pyplot as plt
import csv
import copy
import numpy as np

folder = "test"
file = "log.csv"

headers = None

with open(folder + "/headers.csv", 'r') as csvfile:
    headers1 = csv.reader(csvfile, delimiter=",")
    for row in headers1:
        headers = row

print(headers)


class ContainerElement:
    label = "",
    key = "",
    color = "",
    marker = None,
    index = -1,
    data = []


m = [
    {
        'label': 'x',
        'key': 'timestamp',
        'color': ''
    },
    {
        'label': 'y',
        'key': 'calibratedHeading',
        'color': 'blue'
    },
    {
        'label': 'yp',
        'key': 'gyroHeading',
        'marker': '+',
        'color': 'red'
    },
    {
        'label': 'yref',
        'key': 'compassHeading',
        'color': 'green'
    }
]

mc = []

for (index, e) in enumerate(m):
    new_elem = ContainerElement()
    new_elem.key = e['key']
    new_elem.label = e['label']
    new_elem.color = e['color']
    if 'marker' in e:
        new_elem.marker = e['marker']
    else:
        new_elem.marker = None
        # print(e['marker'])
    for (index2, h) in enumerate(headers):
        if h == new_elem.key:
            new_elem.index = index2
            # e['index'] = index
            break
    new_elem.data = []
    mc.append(new_elem)

print(', '.join(str(e.index) for e in mc))


with open(folder + "/" + file, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        row_length = len(row)
        # print(row)
        for (index, e) in enumerate(mc):
            if e.index != -1 and e.index < row_length:
                d = float(row[e.index])
                e.data.append(d)

plt.gca().set_color_cycle([e.color for e in mc])

x = mc[0].data

x1 = np.array(x)
x1 = (x1 - np.min(x1))/1000
x = list(x1)

samples = None
# samples = 1000

if samples is not None:
    x = x[0:samples]


for (index, e) in enumerate(mc):

    if index != 0:

        if samples is not None:
            e.data = e.data[0:samples]

        # print(e.key)
        if e.marker is not None:
            plt.plot(x, e.data, label=e.label, marker=e.marker)
        else:
            plt.plot(x, e.data, label=e.label)

plt.xlabel('time (s)')
plt.ylabel('y')

# plt.legend(['y', 'yp', 'yref'], loc='upper left')

plt.title('Experimental data')
plt.legend()
plt.show()