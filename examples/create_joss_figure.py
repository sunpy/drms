"""
This example creates the figure shown in the JOSS paper.
"""
from __future__ import absolute_import, division, print_function
import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from astropy.io import fits
import example_helpers
import drms

import pandas
pandas_version = tuple(map(int, pandas.__version__.split('.')[:2]))
if pandas_version >= (0, 22):
    # Since pandas v0.22, we need to explicitely register matplotlib
    # converters to use pandas.Timestamp objects in plots.
    pandas.plotting.register_matplotlib_converters()


def read_fits_data(fname):
    """Reads FITS data and fixes/ignores any non-standard FITS keywords."""
    hdulist = fits.open(fname)
    hdulist.verify('silentfix+warn')
    return hdulist[1].data

# Print the doc string of this example.
print(__doc__)

# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
#
# You will be asked for your registered email address during execution of
# this example. If you don't want to enter it every time you run this script,
# you can set the environment variable JSOC_EXPORT_EMAIL or the variable
# below to your registered email address.
email = ''

# Should the plots been shown and/or saved?
save_plots = True
show_plots = True

# Series, harpnum and segment selection
series = 'hmi.sharp_720s'
sharpnum = 4315
segments = ['magnetogram', 'continuum']
fname_fmt_str = '{series}.{sharpnum}.{tstr}.{segment}.fits'

# Download directory
out_dir = os.path.join('downloads', 'sharp_joss')

# Create download directory if it does not exist yet.
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Keywords to be queried
kwlist = ['T_REC', 'LON_FWT', 'CROTA2', 'AREA_ACR', 'USFLUX', 'ERRVF',
          'CRPIX1', 'CRPIX2', 'CDELT1', 'CDELT2', 'CRVAL1', 'CRVAL2']

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

print('Querying metadata...')
kw = c.query('%s[%d]' % (series, sharpnum), key=kwlist, rec_index=True)
t = drms.to_datetime(kw.T_REC)

print('Finding central meridian crossing...')
rec_cm = kw.LON_FWT.abs().idxmin()
k_cm = kw.loc[rec_cm]
t_cm = drms.to_datetime(kw.T_REC[rec_cm])
print('-> rec_cm:', rec_cm, '@', kw.LON_FWT[rec_cm], 'deg')

# Check if any files were already downloaded.
fnames = {}
download_segments = []
t_cm_str = t_cm.strftime('%Y%m%d_%H%M%S_TAI')
for s in segments:
    fnames[s] = fname_fmt_str.format(
        series=series, sharpnum=sharpnum, tstr=t_cm_str, segment=s)
    if not os.path.exists(os.path.join(out_dir, fnames[s])):
        download_segments.append(s)

# Only download missing files.
if download_segments:
    print()
    if not email:
        email = example_helpers.get_export_email()
    if not email or not c.check_email(email):
        raise RuntimeError('Email address is not valid or not registered.')
    print('Downloading files...')
    export_query = '%s{%s}' % (rec_cm, ','.join(download_segments))
    r = c.export(export_query, email=email)
    dl = r.download(out_dir)
    print()

print('Reading image files...')
data_mag = read_fits_data(os.path.join(out_dir, fnames['magnetogram']))
data_cont = read_fits_data(os.path.join(out_dir, fnames['continuum']))

print('Creating plots...')
plt.rc('figure', figsize=(11, 6.75))
plt.rc('axes', titlesize='medium')
plt.rc('axes.formatter', use_mathtext=True)
plt.rc('mathtext', default='regular')
plt.rc('legend', fontsize='medium', framealpha=1.0)
plt.rc('image', origin='lower', interpolation='none', cmap='gray')

# Convert pixel to world coordinates using WCS keywords
ny, nx = data_mag.shape
xmin = (1 - k_cm.CRPIX1)*k_cm.CDELT1 + k_cm.CRVAL1
xmax = (nx - k_cm.CRPIX1)*k_cm.CDELT1 + k_cm.CRVAL1
ymin = (1 - k_cm.CRPIX2)*k_cm.CDELT2 + k_cm.CRVAL2
ymax = (ny - k_cm.CRPIX2)*k_cm.CDELT2 + k_cm.CRVAL2

# We assume a CROTA2 value close to 180 degree, so we can approximate the
# rotation by inverting the image axes.
if abs(180 - k_cm.CROTA2) < 0.1:
    data_mag = data_mag[::-1, ::-1]
    data_cont = data_cont[::-1, ::-1]
    xmin, xmax = -xmax, -xmin
    ymin, ymax = -ymax, -ymin
else:
    raise RuntimeError('CROTA2 = %.2f value not supported.' % k_cm.CROTA2)

# Compute the image extent used for imshow
extent = (xmin - abs(k_cm.CDELT1)/2, xmax + abs(k_cm.CDELT1)/2,
          ymin - abs(k_cm.CDELT2)/2, ymax + abs(k_cm.CDELT2)/2)

# Create figure with 2x2 axes, with enough space for colorbars on the right
fig, ax = plt.subplots(
    2, 2, num=1, clear=True,
    gridspec_kw={'width_ratios': (2, 2.5)})
ax_meta, ax_img = ax[:, 0], ax[:, 1]

# Create metadata line plots in the left column
# Note: t.values is used for errorbar() because of an issue with pandas < 0.24
axi = ax_meta[0]
axi.errorbar(t.values, kw.USFLUX/1e22, yerr=kw.ERRVF/1e22, fmt='.', ms=2,
             capsize=0, label='USFLUX')
axi.set_title('Total unsigned flux')
axi.set_ylabel(r'Mx $\times 10^{\minus 22}$')

axi = ax_meta[1]
axi.plot(t, kw.AREA_ACR/1e3, '.', ms=2, label='AREA_ACR')
axi.set_title('LoS area of active pixels')
axi.set_ylabel(r'$\mu$Hem $\times 1000$')

ax_meta[0].set_xticklabels([])
ax_meta[1].xaxis.set_major_locator(dates.AutoDateLocator())
ax_meta[1].xaxis.set_major_formatter(dates.DateFormatter('%b\n%d'))
ax_meta[1].set_xlabel('Date')

for axi in ax_meta:
    axi.axvline(t_cm, ls='--', color='tab:orange')
    axi.legend(loc='upper left', numpoints=1)

# Create image plots in the right column
axi = ax_img[0]
axi.set_title('Continuum intensity')
im = axi.imshow(data_cont/1e3, extent=extent, vmax=61)
cb = plt.colorbar(im, ax=axi, label=r'$I_{\mathrm{c}}$ [kDN/s]', pad=0.03)

axi = ax_img[1]
axi.set_title('LoS magnetogram')
im = axi.imshow(data_mag/1e3, extent=extent, vmin=-1, vmax=1)
cb = plt.colorbar(im, ax=axi, label=r'$B_{\mathrm{los}}$ [kG]', pad=0.03)
cb.set_ticks([-1, -0.5, 0, 0.5, 1, 2])

for axi in ax_img:
    axi.set_xlim(-130, 141)
    axi.set_ylim(-262, -86)
    axi.locator_params(axis='y', nbins=4)

ax_img[0].set_xticklabels([])
ax_img[1].set_xlabel('Solar X [arcsec]')
ax_img[0].set_ylabel('Solar Y [arcsec]')
ax_img[1].set_ylabel('Solar Y [arcsec]')

# Make better use of figure space
fig.tight_layout(pad=1.2, w_pad=2)
plt.draw()

if save_plots:
    print('Saving figure...')
    fig.savefig('joss_figure.pdf', dpi=200)

if show_plots:
    print('Showing figure...')
    plt.show()
