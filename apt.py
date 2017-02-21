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
from matplotlib.dates import DayLocator, MonthLocator, WeekdayLocator, DateFormatter

'''
Plots an Annual Prayer Times Chart for a given city, year and a calculation method.

'''

## Needed Configuration ----------------------
cnf_year = 2017
cnf_calc_method = 'Egypt'
cnf_city_name = 'Cairo'
cnf_city_coord = (30.0444, 31.2357)
cnf_tz = 2
## Do not edit below -------------------------

def mock(**kwargs): return type('',(),kwargs)()

PT = PrayTimes(cnf_calc_method)

def time2minutes(time):
    t1 = DT.datetime.strptime(time, '%H:%M')
    t2 = DT.datetime(1900,1,1)
    return((t1-t2).total_seconds() / 3600.0)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(cnf_year, 1, 1)
end_date = date((cnf_year+1), 1, 1)

times = []
t = []
for single_date in daterange(start_date, end_date):
    times.append(PT.getTimes(single_date.timetuple(), cnf_city_coord, cnf_tz))
    t.append(single_date.toordinal())


fajr = [time2minutes(x['fajr']) for x in times]
sunrise = [time2minutes(x['sunrise']) for x in times]
dhuhr = [time2minutes(x['dhuhr']) for x in times]
asr = [time2minutes(x['asr']) for x in times]
maghrib = [time2minutes(x['maghrib']) for x in times]
isha = [time2minutes(x['isha']) for x in times]

# Date Locators
everyday = DayLocator(interval=1)
fridays = WeekdayLocator(FRIDAY)
months = MonthLocator(range(1, 13), bymonthday=1, interval=1) # every month
monthsFmt = DateFormatter("%b '%y")
daysFmt = DateFormatter("%d %b")

fig, ax = plt.subplots()
plt.plot(t,fajr, 'k',t,sunrise, 'k',t,dhuhr, 'k',t,asr, 'k',t,maghrib, 'k',t,isha, 'k')
ax.xaxis.set_major_locator(fridays)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(everyday)
ax.xaxis_date()
ax.autoscale_view()
ax.xaxis.grid(True, 'major')
ax.xaxis.grid(False, 'minor')
ax.set_title('Annual Prayer Times for '+cnf_city_name+', '+str(cnf_year))
#fig.autofmt_xdate() #Autorotate labels
labels = plt.xticks()[1]
plt.setp(labels, rotation=90)
plt.axis([t[0], t[364], 0, 24])
plt.yticks(range(0, 24), fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter('{:}:00'.format))
plt.grid(True, 'major', 'y', ls='-', lw=.5, c='k', alpha=.3)
fig.subplots_adjust(left=0.04,right=0.95)

# Make the shaded regions
# Color set from: https://www.design-seeds.com/seasons/summer/color-set14
regions = []
regions.append(mock(vert= [(t[0], 0)] + list(zip(t, fajr)) + [(t[364], 0)] ,color='#1C818C')) #darklow
regions.append(mock(vert= [(t[0], 24)] + list(zip(t, isha)) + [(t[364], 24)] ,color= '#1C818C')) #darkhi
regions.append(mock(vert=  list(zip(t, sunrise)) + list(zip(t[::-1], fajr[::-1])) ,color= '#7BBED1')) #sunrise
regions.append(mock(vert=  list(zip(t, dhuhr)) + list(zip(t[::-1], sunrise[::-1])) ,color= '#B9D8DE')) #dhuhr
regions.append(mock(vert=  list(zip(t, asr)) + list(zip(t[::-1], dhuhr[::-1])) ,color= '#FAE49E')) #asr
regions.append(mock(vert=  list(zip(t, maghrib)) + list(zip(t[::-1], asr[::-1])) ,color= '#F0A471')) #maghrib
regions.append(mock(vert=  list(zip(t, isha)) + list(zip(t[::-1], maghrib[::-1])) ,color= '#C26642')) #isha

# Make Righside Athan Labels
xpos = t[364]+1
plt.text(xpos,fajr[364],'Fajr')
plt.text(xpos,dhuhr[364],'Dhuhr')
plt.text(xpos,asr[364],'Asr')
plt.text(xpos,maghrib[364],'Maghrib')
plt.text(xpos,isha[364],'Ishaa')

for r in regions:
    poly = Polygon(r.vert, facecolor=r.color, edgecolor=r.color)
    ax.add_patch(poly)

plt.show()
