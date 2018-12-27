import matplotlib.pyplot as plt
import csv

x = []
y = []
yp = []
yref = []

folder = "test"
file = "log.csv"
with open(folder + "/" + file,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        # print(row)
        row_length = len(row)
        x.append(float(row[row_length-1]))
        y.append(float(row[0]))
        yp.append(float(row[4]))
        yref.append(float(row[1]))

plt.gca().set_color_cycle(['blue', 'red', 'green'])
plt.plot(x, y, label='y')
plt.plot(x, yp, label='yp', marker='+')
plt.plot(x, yp, label='yref')
plt.xlabel('x')
plt.ylabel('y')

# plt.legend(['y', 'yp', 'yref'], loc='upper left')

plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()