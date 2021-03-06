# code copied from snag/__init__.py
# create_namelist

import yaml
import datetime as dt
from six import string_types

from snag.namelist import Namelist
from snag.serialize import dump
from snag.utils import merge_dicts
from snag.version import version as __version__

from logging import basicConfig
from utils import make_regular_timeseries
basicConfig()

num_days = 6  # number of days in input file
out_dt = 1800  # timestep (s) of input data

datetime_list = make_regular_timeseries(dt.datetime(2016, 1, 1), dt.datetime(2016, 1, 15), 86400)

for ii, i in enumerate(range(0,len(datetime_list),num_days-1)):
    dt1 = datetime_list[i]

    conf = 'D:/code-GitHub/snag/examples/mcmurdo_land.yml'

    if isinstance(conf, string_types):
        conf = yaml.load(open(conf))

    conf['data']['filename'] = 'T:/DSC-SCM/SCM_INPUT/ver2/Blended_ARM_data_{}{:02}{:02}_{}d_{}s.nc'.format(dt1.year, dt1.month, dt1.day,num_days,out_dt)
    conf['INDATA']['year_init'] = int(dt1.year)
    conf['INDATA']['month_init'] = int(dt1.month)
    conf['INDATA']['day_init'] = int(dt1.day)
    conf['INDATA']['min_init'] = 30
    conf['INDATA']['sec_init'] = 0
    conf['CNTLSCM']['nfor'] = 288
    conf['RUNDATA']['ndayin'] = 5
    conf['RUNDATA']['nminin'] = 1410

    nl = Namelist(conf)
    #nl.variables['w'][:] = 0

    # set all vertical fluxes to 0 for test case
    nl.config['INPROF']['wi'][:] = 0
    nl.config['INPROF']['w_advi'][:] = 0
    nl.config['INOBSFOR']['w_inc'][:] = 0
    nl.config['INOBSFOR']['w_bg'][:] = 0

    try:
        nl.validate()
    except:
        pass

    # dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/namelist_ARM_MCMURDO_land_{}{:02}{:02}_30min.scm'.format(dt1.year, dt1.month, dt1.day), 'w'))
    dump(nl.as_dict(), stream=open('P:/Projects/DSC-SCM/SNAG/ensemble_namelists/group03/namelist_ARM_MCMURDO_land_{:01}.scm'.format(ii), 'w'))
# plot

# import matplotlib.pylab as plt
# import numpy as np
#
# plt.plot(nl.config['INPROF']['qi'])
# plt.plot(nl.config['INPROF']['theta'])
# plt.plot(nl.config['INPROF']['ui'])
# plt.plot(nl.config['INPROF']['vi'])
# plt.plot(nl.config['INPROF']['wi'])
#
#
# plt.imshow(np.transpose(nl.config['INOBSFOR']['t_inc']),origin=0)
#
# plt.colorbar()
#
# plt.close()

