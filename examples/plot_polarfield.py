"""
================================================
Downloading and plotting a HMI polar field data
================================================

This example shows how to download HMI polar field data from JSOC and make a plot.
"""

import matplotlib.pyplot as plt
import numpy as np

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client()

###############################################################################
# Construct the DRMS query string: "Series[timespan][wavelength]"

qstr = 'hmi.meanpf_720s[2010.05.01_TAI-2016.04.01_TAI@12h]'

# Send request to the DRMS server
print('Querying keyword data...\n -> {qstr}')
result = client.query(qstr, key=['T_REC', 'CAPN2', 'CAPS2'])
print(f' -> {len(result)} lines retrieved.')

# Convert T_REC strings to datetime and use it as index for the series
result.index = drms.to_datetime(result.pop('T_REC'))

# Determine smallest timestep
dt = np.diff(result.index.to_pydatetime()).min()

# Make sure the time series contains all time steps (fills gaps with NaNs)
a = result.asfreq(dt)

###############################################################################
# Plot the magnetic field values.

# Compute 30d moving average and standard deviation using a boxcar window
win_size = int(30 * 24 * 3600 / dt.total_seconds())
a_avg = a.rolling(win_size, min_periods=1, center=True).mean()
a_std = a.rolling(win_size, min_periods=1, center=True).std()

# Plot results
t = a.index.to_pydatetime()
n, mn, sn = a.CAPN2, a_avg.CAPN2, a_std.CAPN2
s, ms, ss = a.CAPS2, a_avg.CAPS2, a_std.CAPS2

# Plot smoothed data
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
ax.set_title(qstr, fontsize='medium')
ax.plot(t, n, 'b', alpha=0.5, label='North pole')
ax.plot(t, s, 'g', alpha=0.5, label='South pole')
ax.plot(t, mn, 'r', label='Moving average')
ax.plot(t, ms, 'r', label="")
ax.set_xlabel('Time')
ax.set_ylabel('Mean radial field strength [G]')
ax.legend()
fig.tight_layout()

# Plot raw data
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
ax.set_title(qstr, fontsize='medium')
ax.fill_between(t, mn - sn, mn + sn, edgecolor='none', facecolor='b', alpha=0.3, interpolate=True)
ax.fill_between(t, ms - ss, ms + ss, edgecolor='none', facecolor='g', alpha=0.3, interpolate=True)
ax.plot(t, mn, 'b', label='North pole')
ax.plot(t, ms, 'g', label='South pole')
ax.set_xlabel('Time')
ax.set_ylabel('Mean radial field strength [G]')
ax.legend()
fig.tight_layout()

plt.show()
