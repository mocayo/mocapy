#coding=utf-8

import pickle

from sqlConnect import MSSQL

def dumpPointData(table='T_ZB_PL_RES1',point='C4-A22-PL-01',component='r1'):
	sql = "SELECT DISTINCT	DT,	WL,	realVal FROM LCRiver_xwdh_3.dbo." + table
	sql += " WHERE INSTR_NO = '" + point + "' AND component = '" + component + "'"
 	
	ms = MSSQL()
	print sql
	resList =  ms.ExecQuery(sql)

	output = open(point + '%' + component + '.pkl', 'wb')
	pickle.dump(resList, output)
	return resList

def main():
	# data = pickle.load(open('C4-A22-PL-01%r1.pkl', 'rb'))

	# for i in range(5):print data[i]

	dumpPointData(table='T_ZB_JZ_RES1',point='C4-A09-J-01',component='r1')

if __name__ == '__main__':
    main()