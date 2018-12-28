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
    key = None,
    color = "",
    plot = True,
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
        'disp': False,
        'color': 'blue'
    },
    {
        'label': 'yp',
        'key': 'gyroHeading',
        'disp': True,
        'marker': '+',
        'color': 'red'
    },
    {
        'label': 'yref',
        'key': 'compassHeading',
        'disp': True,
        'color': 'green'
    },
    {
        'label': 'diff',
        'disp': False,
        'color': 'green'
    }
]


def get_mc_by_key(mc, key):
    for m in mc:
        if m.key == key:
            return m
    return None

def get_mc_by_label(mc, key):
    for m in mc:
        if m.label == key:
            return m
    return None

mc = []

for (index, e) in enumerate(m):
    new_elem = ContainerElement()

    if 'key' in e:
        new_elem.key = e['key']

    new_elem.label = e['label']
    new_elem.color = e['color']

    if 'disp' in e:
        new_elem.plot = e['disp']
    else:
        new_elem.plot = False

    if 'marker' in e:
        new_elem.marker = e['marker']
    else:
        new_elem.marker = None
        # print(e['marker'])
    new_elem.index = -1
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


diff = get_mc_by_label(mc, 'diff')
d1 = get_mc_by_key(mc, 'compassHeading')
d2 = get_mc_by_key(mc, 'gyroHeading')
d1 = np.array(d1.data)
d2 = np.array(d2.data)
diff.data = list(d2 - d1)

samples = None
# samples = 1000

if samples is not None:
    x = x[0:samples]


for (index, e) in enumerate(mc):

    if index != 0:

        if samples is not None:
            e.data = e.data[0:samples]

        # print(e.key)
        if e.plot:
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