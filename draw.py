# coding=utf-8

import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

from getData import dumpPointData

data = pickle.load(open('C4-A22-PL-01%r1.pkl', 'rb'))

dt = []
wl = []
val = []

for i in range(30):
    dt.append(data[i][0])
    wl.append(data[i][1])
    val.append(data[i][2])

bar_width = 0.35
wlmax = int(max(wl)) + 5
wlmin = int(min(wl)) - 5
fig, ax = plt.subplots()

# ax.set_xticklabels([day.strftime('%Y-%m-%d') for day in dt],rotation=45)

plt.bar(dt, wl, bar_width, alpha=0.4)
plt.xlabel('date')
plt.ylabel('waterlevel')
plt.ylim(1180, wlmax)
plt.yticks(range(1180, wlmax, 5))

# Tell matplotlib to interpret the x-axis values as dates
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))

# Make space for and rotate the x-axis tick labels
fig.autofmt_xdate()

plt.show()
