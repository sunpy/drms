import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from astropy.io import fits
import pandas
import drms


def read_fits_data(fname):
    """Reads FITS data and fixes/ignores any non-standard FITS keywords."""
    hdulist = fits.open(fname)
    hdulist.verify('silentfix+warn')
    return hdulist[1].data


do_download = 1
save_plots = 1
show_plots = 0

export_email = 'myname@example.com'
series = 'hmi.sharp_720s'
sharpnum = 4315
segments = ['magnetogram', 'continuum']
# segments = ['magnetogram', 'field', 'continuum', 'Dopplergram']
fname_fmt_str = '{series}.{sharpnum}.{tstr}.{segment}.fits'

kwlist = ['T_REC', 'LON_FWT', 'OBS_VR', 'CROTA2',
          'CRPIX1', 'CRPIX2', 'CDELT1', 'CDELT2', 'CRVAL1', 'CRVAL2',
          'AREA_ACR', 'MEANGAM', 'USFLUX', 'ERRVF', 'MEANJZH', 'ERRMIH']

if do_download:
    c = drms.Client(email=export_email)
else:
    c = drms.Client('kis')

print('Querying metadata...')
si = c.info(series)
kw = c.query('%s[%d]' % (series, sharpnum), key=kwlist, rec_index=True)
t = drms.to_datetime(kw.T_REC)

print('Finding central meridian crossing...')
rec_cm = kw.LON_FWT.abs().idxmin()
k_cm = kw.loc[rec_cm]
t_cm = drms.to_datetime(kw.T_REC[rec_cm])
print('-> rec_cm:', rec_cm, '@', kw.LON_FWT[rec_cm], 'deg')

# Generate filenames to check if the files are already downloaded.
t_cm_str = t_cm.strftime('%Y%m%d_%H%M%S_TAI')
fnames = {
    s: fname_fmt_str.format(
        series=series, sharpnum=sharpnum, tstr=t_cm_str, segment=s)
    for s in segments}

# Check if any files were already downloaded and download them if not.
download_segments = []
for k, v in fnames.items():
    if not os.path.exists(v):
        download_segments.append(k)
if do_download and download_segments:
    print('Downloading files...')
    exp_query = '%s{%s}' % (rec_cm, ','.join(download_segments))
    r = c.export(exp_query)
    dl = r.download('.', verbose=True)


print('Reading data files...')
data = {
    s: read_fits_data(fnames[s])
    for s in segments}

# Remove observer's LOS velocity
if 'Dopplergram' in data:
    data['Dopplergram'] -= k_cm.OBS_VR

# Convert pixel to world coordinates using WCS keywords
ny, nx = data[segments[0]].shape
xmin = (1 - k_cm.CRPIX1)*k_cm.CDELT1 + k_cm.CRVAL1
xmax = (nx - k_cm.CRPIX1)*k_cm.CDELT1 + k_cm.CRVAL1
ymin = (1 - k_cm.CRPIX2)*k_cm.CDELT2 + k_cm.CRVAL2
ymax = (ny - k_cm.CRPIX2)*k_cm.CDELT2 + k_cm.CRVAL2

# We assume a CROTA2 value close to 180 degree, so we can approximate the
# rotation by inverting the image axes.
if abs(180 - k_cm.CROTA2) < 0.1:
    for s in segments:
        data[s] = data[s][::-1, ::-1]
    xmin, xmax = -xmax, -xmin
    ymin, ymax = -ymax, -ymin
else:
    raise RuntimeError('CROTA2 = %.2f value not supported.' % k_cm.CROTA2)

# Compute the image extent used for imshow
extent = (xmin - abs(k_cm.CDELT1)/2, xmax + abs(k_cm.CDELT1)/2,
          ymin - abs(k_cm.CDELT2)/2, ymax + abs(k_cm.CDELT2)/2)


print('Creating plots...')
plt.rc('figure', figsize=(11, 6.75))
plt.rc('axes', titlesize='medium')
plt.rc('axes.formatter', use_mathtext=True)
plt.rc('mathtext', default='regular')
plt.rc('legend', fontsize='medium', framealpha=1.0)
plt.rc('image', origin='lower', interpolation='none', cmap='gray')
pandas.plotting.register_matplotlib_converters()

fig, ax = plt.subplots(
    2, 2, num=1, clear=True,
    gridspec_kw={'width_ratios': (2, 2.5)})
ax_meta, ax_img = ax[:, 0], ax[:, 1]

###

axi = ax_meta[1]
axi.plot(t, kw.AREA_ACR/1e3, '.', ms=2, label='AREA_ACR')
axi.set_title('LoS area of active pixels')
axi.set_ylabel(r'$\mu$Hem $\times 1000$')

# axi = ax_meta[1]
# axi.plot(t, kw.MEANGAM, '.', ms=2, label='MEANGAM')
# axi.set_title('Mean inclination angle')
# axi.set_ylabel('degree')

axi = ax_meta[0]
axi.errorbar(t, kw.USFLUX/1e22, yerr=kw.ERRVF/1e22, fmt='.', ms=2,
             capsize=0, label='USFLUX')
axi.set_title('Total unsigned flux')
axi.set_ylabel(r'Mx $\times 10^{\minus 22}$')

# axi = ax_meta[1]
# axi.errorbar(t, kw.MEANJZH*1e3, yerr=kw.ERRMIH*1e3, fmt='.', ms=2,
#              capsize=0, label='MEANJZH')
# axi.set_title('Mean current helicity')
# axi.set_ylabel(r'G$^2$ m$^{\minus 1}$ $\times 1000$')

ax_meta[0].set_xticklabels([])
ax_meta[1].xaxis.set_major_locator(dates.AutoDateLocator())
ax_meta[1].xaxis.set_major_formatter(dates.DateFormatter('%b\n%d'))
ax_meta[1].set_xlabel('Date')

for axi in ax_meta:
    axi.axvline(t_cm, ls='--', color='tab:orange')
    axi.legend(loc='upper left', numpoints=1)

###

axi = ax_img[1]
di = data['magnetogram']
axi.set_title('LoS magnetogram')
im = axi.imshow(di/1e3, extent=extent, vmin=-1, vmax=1)
cb = plt.colorbar(im, ax=axi, label=r'$B_{\mathrm{los}}$ [kG]', pad=0.03)
cb.set_ticks([-1, -0.5, 0, 0.5, 1, 2])

axi = ax_img[0]
di = data['continuum']
axi.set_title('Continuum intensity')
im = axi.imshow(di/1e3, extent=extent, vmax=61)
cb = plt.colorbar(im, ax=axi, label=r'$I_{\mathrm{c}}$ [kDN/s]', pad=0.03)

# axi = ax_img[0]
# di = data['field']
# axi.set_title('Magnetic field strength')
# im = axi.imshow(di/1e3, extent=extent, vmin=0.05, vmax=2.6)
# cb = plt.colorbar(im, ax=axi, label=r'$|B|$ [kG]')

# axi = ax_img[1]
# di = data['Dopplergram']
# axi.set_title('LoS Doppler velocity')
# im = axi.imshow(di/1e3, extent=extent, vmin=-1.3, vmax=1.3)
# cb = plt.colorbar(im, ax=axi, label=r'$v_{\mathrm{los}}$ [km/s]')

for axi in ax_img:
    axi.set_xlim(-130, 141)
    axi.set_ylim(-262, -86)
    axi.locator_params(axis='y', nbins=4)

ax_img[0].set_xticklabels([])
ax_img[1].set_xlabel('Solar X [arcsec]')
ax_img[0].set_ylabel('Solar Y [arcsec]')
ax_img[1].set_ylabel('Solar Y [arcsec]')

###

fig.tight_layout(pad=1.2, w_pad=2)
plt.draw()

if save_plots:
    print('Saving plots...')
    fig.savefig('sharp.pdf', dpi=200)
    fig.savefig('sharp.png', dpi=200)

if show_plots:
    plt.show()
