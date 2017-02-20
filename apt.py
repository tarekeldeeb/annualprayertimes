#!/usr/bin/env python
# compatible with python 2.x and 3.x

import math
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import datetime as DT
from datetime import timedelta, date
from pt import *

def mock(**kwargs): return type('',(),kwargs)()

PT = PrayTimes('Egypt')

def time2minutes(time):
    t1 = DT.datetime.strptime(time, '%H:%M')
    t2 = DT.datetime(1900,1,1)
    return((t1-t2).total_seconds() / 3600.0)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2017, 1, 1)
end_date = date(2018, 1, 1)
d=0
times = []
#t = []
for single_date in daterange(start_date, end_date):
    times.append(PT.getTimes(single_date.timetuple(), (30.044, 31.2357), 2))
    #t.append(single_date.strftime("%Y-%m-%d"))
    #print (single_date.strftime("%Y-%m-%d") + " : " + times[d]['fajr'])
    d = d+1

t = np.arange(1, 366)
fajr = [time2minutes(x['fajr']) for x in times]
sunrise = [time2minutes(x['sunrise']) for x in times]
dhuhr = [time2minutes(x['dhuhr']) for x in times]
asr = [time2minutes(x['asr']) for x in times]
maghrib = [time2minutes(x['maghrib']) for x in times]
isha = [time2minutes(x['isha']) for x in times]

#print "T=", len(t), "fajr=", len(fajr)

fig, ax = plt.subplots()
plt.plot(t,fajr, '#0d2bbb',t,sunrise, '#efe000',t,dhuhr, 'r',t,asr, '#94ff00',t,maghrib, '#ff7b00',t,isha, 'k')
#ax.plot_date(t,fajr, 'k')
plt.axis([1, 365, 0, 24])

plt.yticks(range(0, 24), fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter('{:}:00'.format))
plt.grid(True, 'major', 'y', ls='-', lw=.5, c='k', alpha=.3)


# Make the shaded regions
regions = []
regions.append(mock(vert= [(1, 0)] + list(zip(t, fajr)) + [(365, 0)] ,color='0.3')) #darklow
regions.append(mock(vert= [(1, 24)] + list(zip(t, isha)) + [(365, 24)] ,color= '0.3')) #darkhi
fajr_r = fajr[::-1]
t_r = t[::-1]
regions.append(mock(vert=  list(zip(t, sunrise)) + list(zip(t_r, fajr_r)) ,color= '#efe000')) #sunrise

for r in regions:
    poly = Polygon(r.vert, facecolor=r.color, edgecolor=r.color)
    ax.add_patch(poly)

plt.show()