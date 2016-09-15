from __future__ import absolute_import, division, print_function
from pylab import *
import pandas as pd
import example_helpers
import drms


# Series name, time range and time steps
series = 'hmi.meanpf_720s'
tsel = '2010.05.01_TAI-2016.04.01_TAI@12h'

# DRMS query string
qstr = '%s[%s]' % (series, tsel)


# Create DRMS JSON client, use debug=True to see the query URLs
c = drms.Client()

# Send request to the DRMS server
print('Querying keyword data...\n -> %s' % qstr)
res = c.query(qstr, key=['T_REC', 'CAPN2', 'CAPS2'])
print(' -> %d lines retrieved.' % len(res))

# Convert T_REC strings to datetime and use it as index for the series
res.index = drms.to_datetime(res.pop('T_REC'))

# Determine smallest timestep
dt = diff(res.index.to_pydatetime()).min()

# Make sure the time series contains all time steps (fills gaps with NaNs)
# Note: This does not seem to work with old pandas versions (e.g. v0.14.1)
a = res.asfreq(dt)

# Compute 30d moving average and standard deviation using a boxcar window
win_size = int(30*24*3600/dt.total_seconds())
if tuple(map(int, pd.__version__.split('.')[:2])) >= (0, 18):
    a_avg = a.rolling(win_size, min_periods=1, center=True).mean()
    a_std = a.rolling(win_size, min_periods=1, center=True).std()
else:
    # this is deprecated since pandas v0.18.0
    a_avg = pd.rolling_mean(a, win_size, min_periods=1, center=True)
    a_std = pd.rolling_std(a, win_size, min_periods=1, center=True)

# Plot results
t = a.index.to_pydatetime()
n, mn, sn = a.CAPN2, a_avg.CAPN2, a_std.CAPN2
s, ms, ss = a.CAPS2, a_avg.CAPS2, a_std.CAPS2

figure(1, figsize=(15, 7)); clf()
title(qstr, fontsize='medium')
plot(t, n, 'b', alpha=0.5, label='North pole')
plot(t, s, 'g', alpha=0.5, label='South pole')
plot(t, mn, 'r', label='Moving average')
plot(t, ms, 'r', label='')
xlabel('Time')
ylabel('Mean radial field strength [G]')
legend()
tight_layout()
draw()

figure(2, figsize=(15, 7)); clf()
title(qstr, fontsize='medium')
plt.fill_between(
    t, mn-sn, mn+sn, edgecolor='none', facecolor='b', alpha=0.3,
    interpolate=True)
plt.fill_between(
    t, ms-ss, ms+ss, edgecolor='none', facecolor='g', alpha=0.3,
    interpolate=True)
plot(t, mn, 'b', label='North pole')
plot(t, ms, 'g', label='South pole')
xlabel('Time')
ylabel('Mean radial field strength [G]')
legend()
tight_layout()
draw()

show()
