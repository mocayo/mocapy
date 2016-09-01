#coding=utf-8

import pickle
import pandas
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.stattools import adfuller as ADF

#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei'] 

#用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False 

alldata = pickle.load(open('C4-A22-PL-01%r1.pkl', 'rb'))

data = alldata[0:30]
dt = [data[i][0].strftime("%Y-%m-%d") for i in range(len(data))]
val = [float(data[i][2]) for i in range(len(data))]

df = pandas.DataFrame(index=dt, data=val, columns=['val'])

acf_fig = plot_acf(df)
acf_fig.savefig('acf_fig.jpg')

pacf_fig = plot_pacf(df)
pacf_fig.savefig('pacf_fig.jpg')

print u'原始序列的ADF检验结果为：', ADF(df['val'])

#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox

#返回统计量和p值
print u'差分序列的白噪声检验结果为：', acorr_ljungbox(df['val'], lags=1)