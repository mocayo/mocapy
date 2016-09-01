# coding=utf-8

import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

mpl.rcParams['font.sans-serif'] = ['Consolas']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
mpl.rc('xtick', labelsize=20)  # 设置坐标轴刻度显示大小
mpl.rc('ytick', labelsize=20)

font_size = 25

data = pickle.load(open('C4-A22-PL-01%r1.pkl', 'rb'))

dt = [data[i][0] for i in range(len(data))]
val = [data[i][2] for i in range(len(data))]
wl = [data[i][1] for i in range(len(data))]

wlmax = int(max(wl[0:30])) + 5
wlmin = int(min(wl[0:30])) - 5

plt.style.use('fivethirtyeight')

fig1 = plt.figure(figsize=(25, 20))
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()

print type(ax1)
print type(ax2)

ax1.plot(dt[0:30], val[0:30], label='realVal' )
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
ax1.set_xlabel('DT', fontsize=font_size)
ax1.set_ylabel('realval', fontsize=font_size)
fig1.autofmt_xdate()

ax2.bar(dt[0:30], wl[0:30], label='waterlevel', alpha=0.4, align='center')
ax2.set_ylim(wlmin, wlmax)
ax2.set_yticks(range(wlmin, wlmax, 5))
ax2.set_ylabel('waterlevel', fontsize=font_size)

legend1 = ax1.legend(loc=(.03, .94), fontsize=16, shadow=True)
legend2 = ax2.legend(loc=(.03, .89), fontsize=16, shadow=True)
legend1.get_frame().set_facecolor('#FFFFFF')
legend2.get_frame().set_facecolor('#FFFFFF')

plt.title('C4-A22-PL-01 r1', fontsize=font_size)
# figname = 'C4-A22-PL-01%r1-30days.png'
# plt.savefig(figname, dpi=300)

plt.show()
