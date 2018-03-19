"""
code to check options specified in yml file are consistent. reads in configuration dictionary (config) before writing to file
"""

import numpy as np


def validate_landpoints(config):
    if config['CNTRLSCM']['landpoints'][:] == 1 and config['LOGIC']['land_sea_mask'][:] == True:
        # print('Land or coastal case chosen')
        pass
    elif config['CNTRLSCM']['landpoints'][:] == 0 and config['LOGIC']['land_sea_mask'][:] == False:
        # print('Sea case chosen')
        pass
    else:
        raise Exception('Incorrect combination of CNTRLSCM:landpoints and LOGIC:land_sea_mask')


def validate_land_ice_soil(config):
    if config['LOGIC']['land_ice_mask'][:] == True and config['LOGIC']['soil_mask'][:] == False:
        print('Land ice subsurface chosen')
    elif config['LOGIC']['land_ice_mask'][:] == False and config['LOGIC']['soil_mask'][:] == True:
        print('Land soil subsurface chosen')
    else:
        raise Exception('Incorrect combination of LOGIC:land_ice_mask and LOGIC:soil_mask')


def validate_fland_ctile(config):
    if config['CNTRLSCM']['landpoints'][:] == 1 and config['RUNDATA']['fland_ctile'][:] == 1:
        print('100% Land case chosen')
    elif config['CNTRLSCM']['landpoints'][:] == 1 and config['RUNDATA']['fland_ctile'][:] > 0 and config['RUNDATA'][
                                                                                                      'fland_ctile'][
                                                                                                  :] < 1:
        print('Coastal case chosen')
    elif config['CNTRLSCM']['landpoints'][:] == 0 and config['RUNDATA']['fland_ctile'][:] == 0:
        print('Sea case chosen')
    else:
        raise Exception('Incorrect combination of CNTRLSCM:landpoints and RUNDATA:fland_ctile')


def validate_soil_type(config):
    if config['CNTRLSCM']['landpoints'][:] == 1 and config['LOGIC']['land_ice_mask'][:] == True and config['INDATA'][
                                                                                                        'soil_type'][
                                                                                                    :] == 1:
        pass
    elif config['CNTRLSCM']['landpoints'][:] == 1 and config['LOGIC']['soil_mask'][:] == True and config['INDATA'][
                                                                                                      'soil_type'][
                                                                                                  :] > 1 and \
            config['INDATA']['soil_type'][:] <= 3:
        pass
    elif config['CNTRLSCM']['landpoints'][:] == 0:
        pass
    else:
        raise Exception('Incorrect combination of LOGIC:land_ice_mask and INDATA:soil_type')


def validate_suface_diag(config):
    # check correct diagnostics output
    if config['CNTRLSCM']['landpoints'][:] == 1 and config['DIAGS']['l_SCMDiag_sea'][:] == False and config['DIAGS'][
                                                                                                         'l_SCMDiag_land'][
                                                                                                     :] == True:
        # print('Land diagnostics output')
        pass
    elif config['CNTRLSCM']['landpoints'][:] == 0 and config['DIAGS']['l_SCMDiag_sea'][:] == True and config['DIAGS'][
                                                                                                          'l_SCMDiag_land'][
                                                                                                      :] == False:
        # print('Sea diagnostics output')
        pass
    else:
        raise Exception('Incorrect value for DIAGS:l_SCMDiag_sea or DIAGS:l_SCMDiag_land')


def validate_number_soil_layers(config):
    # check if soil layers are consistent for soil moisture and temperature. only needed for two options
    if config['INJULES']['smi_opt'] == 0:
        if len(config['INPROF']['t_deep_soili'][:]) != len(config['INJULES']['smcli'][:]):
            raise Exception('different number of soil layers specified in INPROF:t_deep_soili and INJULES:smcli')
    if config['INJULES']['smi_opt'] == 2:
        if len(config['INPROF']['t_deep_soili'][:]) != len(config['INJULES']['sth'][:]):
            raise Exception('different number of soil layers specified in INPROF:t_deep_soili and INJULES:sth')


def validate_length_of_simulation(config):
    forcing_length_s = config['INOBSFOR']['obs_pd'][:] * config['CNTLSCM']['nfor'][:]
    requested_length_s = config['RUNDATA']['ndayin'][:] * 86400 + config['RUNDATA']['nmin'][:] * 60 + config['RUNDATA']['nsecin'][:]
    if int(forcing_length_s ) != int(requested_length_s):
        raise Exception('stated length of forcing data (INOBSFOR:obs_pd * CNTLSCM:nfor does not match days requested in RUNDATA')


def validate_obs_forcing(config):
    # check that observational forcing variables have no nan's and are correct length (nfor * model_levels_nml)
    if config['LOGIC']['obs'][:] == True:
        for var in ['t_inc', 'q_star', 'u_inc', 'v_inc', 'w_inc', 't_bg', 'q_bg', 'u_bg', 'v_bg', 'w_bg']:
            if var in ['w_inc', 'w_bg']: # w forcing has extra layer
                if len(config['INOBSFOR'][var][:]) != (
                        config['CNTRLSCM']['nfor'][:] * (config['CNTRLSCM']['model_levels_nml'][:] + 1)):
                    raise Exception('Incorrect length of forcing variable {}'.format(var))
            elif len(config['INOBSFOR'][var][:]) != (
                    config['CNTRLSCM']['nfor'][:] * config['CNTRLSCM']['model_levels_nml'][:]):
                raise Exception('Incorrect length of forcing variable {}'.format(var))
            if np.any(np.isnan(config['INOBSFOR'][var][:])):
                raise Exception('Nan values in forcing variable {}'.format(var))


def validate_intial_state(config):
    # check that intial state variables have no nan's and are the correct length,
    for var in ['p_in', 'thetai', 'qi', 'ui', 'vi', 'wi', 'w_advi']:
        if len(config['INOBSFOR'][var][:]) != (
                config['CNTRLSCM']['nfor'][:] * config['CNTRLSCM']['model_levels_nml'][:]):
            raise Exception('Incorrect length of forcing variable {}'.format(var))
        if np.any(np.isnan(config['INPROF'][var][:])):
            raise Exception('Nan values in inital profile of {}'.format(var))


def validate_JULES_tiles(config):
    # check the length of JULES tiles:
    for var in ['fract_typ', 'z0_tile','t_star_file','catch','canopy','infil_tile','snow_file','rgrain']:
        if len(config['INJULES'][var][:]) != 9:
            raise Exception('Incorrect length of Jules parameter {}'.format(var))
    for var in ['canht','lai']:
        if len(config['INJULES'][var][:]) != 5:
            raise Exception('Incorrect length of Jules parameter {}'.format(var))
    for var in ['smi_opt','gs']:
        if len(config['INJULES'][var][:]) != 1:
            raise Exception('Incorrect length of Jules parameter {}'.format(var))


def validate_surface_forcing(config):
    if config['LOGIC']['obs_surf'][:] == True:
        # check if at least one variable available
        try:
            config['INOBSFOR']['tstar_forcing']
        except KeyError:
                try:
                    config['INOBSFOR']['flux_h']
                except KeyError:
                    raise Exception('no surface observation forcing (t_star_forcing or flux_h) available')

        # check length of variables that are there
        for var in ['flux_h','flux_e','tstar_forcing']:
            try:
                if len(config['INOBSFOR'][var][:]) != config['CNTRLSCM']['nfor'][:]:
                    raise Exception('surface forcing variables {} does not match nfor'.format(var))
            except KeyError:
                pass

