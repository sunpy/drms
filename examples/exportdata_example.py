import pandas as pd
import drms_json as drms
from astropy.io import fits

# This is an example of how to export files from JSOC using python.

#### Example 1: Export FITS files ####
# Series name, time range and time steps
series = 'hmi.sharp_720s'
tsel = '2016.04.01_TAI'
harpnum = '6464'
segnames = ['magnetogram','field']  # can be a list of one or more segnames 
requestor = 'jschmoe'               # edit this with your own username
notify = 'jschmoe@stanford.edu'     # edit this with your own e-mail address

# DRMS query string
query = '%s[%s][%s]{%s}' % (series, harpnum, tsel, ','.join(segnames))

# Create DRMS JSON client, use debug=True to see the query URLs
drms_url, data_url = 'jsoc', 'http://jsoc.stanford.edu'
c = drms.Client(drms_url)

# Send request to the DRMS server

print('Querying keyword data...\n -> %s' % query)
paths = c.export(query,requestor, notify)

# The following lines will not work if your username and e-mail address are not registered with jsoc.stanford.edu. The lines below will not work with this example code as-is (with requestor = 'jschmoe' and notify = 'jschmoe@stanford.edu'). 

# Read the data segment
# Note: HTTP downloads get cached in ~/.astropy/cache/downloads
for i in range(len(paths)):
    print('Reading data from %s' % paths[i])
    a = fits.open(paths[i])

#### Example 2: Export generic segments, e.g. text files ####

series = 'hmi.rdVflows_fd15_frame'
carrington_rotation = '2097'
longitude = '360'
segnames = 'Ux'                     
requestor = 'jschmoe'               # edit this with your own username
notify = 'jschmoe@stanford.edu'     # edit this with your own e-mail address

# DRMS query string
query = '%s[%s][%s]{%s}' % (series, carrington_rotation, longitude, segnames)

# Create DRMS JSON client, use debug=True to see the query URLs
drms_url, data_url = 'jsoc', 'http://jsoc.stanford.edu'
c = drms.Client(drms_url)

# Send request to the DRMS server
print('Querying keyword data...\n -> %s' % query)
paths = c.export(query,requestor, notify)

# The following lines will not work if your username and e-mail address are not registered with jsoc.stanford.edu. The lines below will not work with this example code as-is (with requestor = 'jschmoe' and notify = 'jschmoe@stanford.edu'). 

# Read the data segment
datafiles = pd.read_html(str(paths[0]),skiprows=2)
data = []
for i in range(datafiles[0][1].shape[0]):
    data.append(pd.read_csv(str(paths[0])+'/'+datafiles[0][1][i]))
