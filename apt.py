#!/usr/bin/env python
# compatible with python 2.x and 3.x

import math
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime as DT
from datetime import timedelta, date

from pt import *

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
for single_date in daterange(start_date, end_date):
    times.append(PT.getTimes(single_date.timetuple(), (30.044, 31.2357), 2))
    print (single_date.strftime("%Y-%m-%d") + " : " + times[d]['fajr'])
    d = d+1

values = [time2minutes(x['fajr']) for x in times]
plt.plot(values, 'r')
plt.show()