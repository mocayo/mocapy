#coding=utf-8

import json
import csv
from sqlConnect import MSSQL

models = [{'id':'2','name':u'插值'},{'id':'3','name':u'拟合'},{'id':'4','name':u'二次多项式'}]

def getTableByPoint(point='C4-A29-PL-01'):
	sql = "SELECT [table] FROM	LCRiver_xwdh_1.dbo.DefTableType "
	sql += "WHERE [type] IN (SELECT [type] FROM LCRiver_xwdh_1.dbo.DefInsSort "
	sql += "WHERE [DesignCode] = '" + point.strip() + "')"
	ms = MSSQL()
	resList =  ms.ExecQuery(sql)
	return "".join(resList[0]).strip()

def getCompByTable(table='T_ZB_PL'):
	sql = "SELECT R1,R2,R3 FROM LCRiver_xwdh_1.dbo.MonitorItemType "
	sql += "WHERE TABLE_NAME = '" + table.strip() + "'"

	ms = MSSQL()
	resList = ms.ExecQuery(sql)
	return resList[0]

def getRByComp(comps,comp):
	for i in range(len(comps)):
		if comp == comps[i]:
			return 'r' + str(i+1)
	return None

def getRByPoint(point,comp):
	table = getTableByPoint(point)
	comps = getCompByTable(table)
	return getRByComp(comps,comp)

def getPrehandleByPoint(point='C4-A29-PL-01', comp='r2', start='2012-06-01', end='2016-04-01'):
	tb = getTableByPoint(point)
	sql = "SELECT DISTINCT dt,prehandle FROM LCRiver_xwdh_3.dbo." + tb + "_RES1 "
	sql += "WHERE instr_no = '" + point.strip()+ "' AND component = '" + comp + "' "
	sql += "AND dt BETWEEN '" + start + "' AND '" + end + "'"
	sql += ' ORDER BY dt'
	# print sql
	ms = MSSQL()
	resList = ms.ExecQuery(sql)
	return resList

def getRealByPoint(point='C4-A29-PL-01', comp='r2', start='2012-06-01', end='2016-04-01'):
	tb = getTableByPoint(point)
	sql = "SELECT DISTINCT dt,realVal FROM LCRiver_xwdh_3.dbo." + tb + "_RES1 "
	sql += "WHERE instr_no = '" + point.strip()+ "' AND component = '" + comp + "' "
	sql += "AND dt BETWEEN '" + start + "' AND '" + end + "'"
	sql += ' ORDER BY dt'
	# print sql
	ms = MSSQL()
	resList = ms.ExecQuery(sql)
	pres = []
	for res in resList:
		preval = res[1]
		if preval == None:
			preval = 0
		pres.append((res[0], float(preval)))

	return pres

def getPredictByPoint(point='C4-A29-PL-01', comp='r2', start='2012-06-01', end='2016-04-01', modelid='2'):
	tb = getTableByPoint(point)
	sql = "SELECT DISTINCT dt,preVal FROM LCRiver_xwdh_3.dbo." + tb + "_RES1 "
	sql += "WHERE instr_no = '" + point.strip()+ "' AND component = '" + comp + "' "
	sql += "AND dt BETWEEN '" + start + "' AND '" + end + "' AND modelId=" + modelid
	sql += ' ORDER BY dt'
	# print sql
	ms = MSSQL()
	resList = ms.ExecQuery(sql)

	pres = []
	for res in resList:
		preval = res[1]
		if preval == None:
			preval = 0
		pres.append((res[0], float(preval)))

	return pres

def writeCSVByPoint(point='C4-A29-PL-01', comp=u'顺河向位移'):
	r = getRByPoint(point,comp)
	pres = getPrehandleByPoint(point=point, comp=r)
	print pres
	if len(pres)==0:
		return
	handles = []
	for pre in pres:
		handleval = pre[1]
		if handleval == None:
			handleval = 0
		if handleval == '':
			handleval = 0
		handles.append((pre[0].strftime('%Y-%m-%d'), float(handleval)))

	csvfile = file('csvs/' + point + '.csv', 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(['dt', r])
	writer.writerows(handles)
	csvfile.close()	

with open('points.json', 'r') as f:
  data = json.load(f)

def draw(datas,point,comp):
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdate

	# 绘图设置
	# 设置字体
	mpl.rcParams['font.sans-serif'] = ['SimHei']  
	# 用来正常显示负号
	mpl.rcParams['axes.unicode_minus'] = False  
	# 设置坐标轴刻度显示大小
	mpl.rc('xtick', labelsize=20)  
	mpl.rc('ytick', labelsize=20)
	# 设置绘图风格
	plt.style.use('ggplot')

	font_size = 12

	# dt = [data[i][0] for i in range(len(data))]
	# realVal = [data[i][1] for i in range(len(data))]
	# preVal = [data[i][2] for i in range(len(data))]

	line_width = 1
	# data_len = len(data)

	fig = plt.figure(figsize=(25, 20))
	ax = fig.add_subplot(111)

	for rawdata in datas:
		data = rawdata[0]
		label = rawdata[1]
		dt = [data[i][0] for i in range(len(data))]
		val = [data[i][1] for i in range(len(data))]
		plt.plot(dt, val, label=label, linewidth=line_width)
	# plt.plot_date(dt[0:data_len], realVal[0:data_len], 'blue', label=u'实测值', linewidth=line_width)
	# plt.plot_date(dt[0:data_len], preVal[0:data_len], 'orange', label=u'预测值', linewidth=line_width)

	ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))

	dtlocator = mdate.MonthLocator(interval=4)
	dtlocator.MAXTICKS = 1500

	ax.xaxis.set_major_locator(dtlocator)
	# fig.autofmt_xdate()
	ax.set_xlabel(u'日期', fontsize=font_size)
	ax.set_ylabel(u'测值', fontsize=font_size)

	for label in ax.xaxis.get_ticklabels():  
	    label.set_fontsize(font_size)  
	for label in ax.yaxis.get_ticklabels():  
	    label.set_fontsize(font_size)   

	plt.legend(fontsize=font_size)
	plt.title(point + comp, fontsize=font_size)
	figname = 'charts/' + point + comp + '.png'
	plt.grid()
	plt.savefig(figname, dpi=300)
	plt.close()
	# plt.show()


def getAllDataByPoint(point='C4-A29-PL-01', comp=u'顺河向位移'):
	r = getRByPoint(point, comp)
	
	real = getRealByPoint(point, r)
	if len(real)==0:
		return
	model2 = getPredictByPoint(point, r, modelid='2')
	model3 = getPredictByPoint(point, r, modelid='3')
	model4 = getPredictByPoint(point, r, modelid='4')

	alldata = [(real,u'实测值'), (model2,u'插值'), (model3,u'拟合'), (model4,u'二次多项式')]
	# print alldata
	draw(alldata, point, comp)

# getAllDataByPoint('C4-A29-J-02',u'开合度')
for i in range(len(data)):
	instr_no = data[i]['instr_no']
	component = data[i]['component']
	print instr_no
	print component
	getAllDataByPoint(instr_no, component)
	print i
	print '-------------------------'