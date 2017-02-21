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
from matplotlib.dates import FRIDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

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


# every monday
fridays = WeekdayLocator(FRIDAY)
# every 2 month
months = MonthLocator(range(1, 13), bymonthday=1, interval=2)
monthsFmt = DateFormatter("%b '%y")

#ax.plot_date(dates, opens, '-')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.xaxis.set_minor_locator(fridays)
ax.autoscale_view()
ax.xaxis.grid(False, 'major')
ax.xaxis.grid(True, 'minor')
#ax.grid(True)

fig.autofmt_xdate()


plt.plot(t,fajr, 'k',t,sunrise, 'k',t,dhuhr, 'k',t,asr, 'k',t,maghrib, 'k',t,isha, 'k')
#ax.plot_date(t,fajr, 'k')
plt.axis([1, 365, 0, 24])

plt.yticks(range(0, 24), fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter('{:}:00'.format))
plt.grid(True, 'major', 'y', ls='-', lw=.5, c='k', alpha=.3)


# Make the shaded regions
# Color set from: https://www.design-seeds.com/seasons/summer/color-set14
regions = []
regions.append(mock(vert= [(1, 0)] + list(zip(t, fajr)) + [(365, 0)] ,color='#1C818C')) #darklow
regions.append(mock(vert= [(1, 24)] + list(zip(t, isha)) + [(365, 24)] ,color= '#1C818C')) #darkhi
regions.append(mock(vert=  list(zip(t, sunrise)) + list(zip(t[::-1], fajr[::-1])) ,color= '#7BBED1')) #sunrise
regions.append(mock(vert=  list(zip(t, dhuhr)) + list(zip(t[::-1], sunrise[::-1])) ,color= '#B9D8DE')) #dhuhr
regions.append(mock(vert=  list(zip(t, asr)) + list(zip(t[::-1], dhuhr[::-1])) ,color= '#FAE49E')) #asr
regions.append(mock(vert=  list(zip(t, maghrib)) + list(zip(t[::-1], asr[::-1])) ,color= '#F0A471')) #maghrib
regions.append(mock(vert=  list(zip(t, isha)) + list(zip(t[::-1], maghrib[::-1])) ,color= '#C26642')) #isha

for r in regions:
    poly = Polygon(r.vert, facecolor=r.color, edgecolor=r.color)
    ax.add_patch(poly)



plt.show()