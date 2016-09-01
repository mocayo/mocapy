#coding: utf-8

import pickle
import numpy as np
import matplotlib.pyplot as pl
from scipy import interpolate 

x = np.linspace(0, 2*np.pi+np.pi/4, 10)
y = np.sin(x)

x_new = np.linspace(0, 2*np.pi+np.pi/4, 100)
f_linear = interpolate.interp1d(x, y)
tck = interpolate.splrep(x, y)
y_bspline = interpolate.splev(x_new, tck)

print f_linear(x_new)
print y_bspline

pl.plot(x, y, "o",  label=u"orignal")
pl.plot(x_new, f_linear(x_new), label=u"line")
pl.plot(x_new, y_bspline, label=u"B-spline")
pl.legend()
pl.show()