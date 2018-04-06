"""This module has various functions that allow the user to 
choose halos in an N-body simulation using various selection
criteria.

Functions
---------
centrals
subhalos

"""

import numpy as np
import pandas as pd
from astropy.table import Table
import grab_files as grab

def centrals(userpath, halofile, mass_range=[1.e12, 1.e15], chunk=100):
    """This function will select all halos in the simulation
    based on the mass range specified.
    This function assumes the halocatalogs are sorted by virial mass.

    Parameters
    ----------
    userpath : string
        the directory path that points to where the outputs will be stored
    halofile : string
        the input halo catalog file
    mass_range : tuple
        min_mass, max_mass

    Returns
    -------
    centrals : pd.DataFrame
        A pandas.DataFrame that contains all of the input columns for the 
        selected central halos.

    """
    #initialize masstest
    assert mass_range[1] > mass_range[0]
    masstest = mass_range[1]
    i = 0

    #grab the halo catalog
    rows = [1, 57]
    read_halo = grab.reader(halofile, skiprows=rows)
    halo_name = halofile.split('/')[-1]

    while masstest >= mass_range[0]:

        datachunk = read_halo.get_chunk(chunk)
        keys = datachunk.keys()
        
        selectcentral = np.where(np.logical_and(datachunk[keys[11]] > mass_range[0],
                                                    datachunk[keys[11]] < mass_range[1]))[0]

        centralchunk = datachunk.iloc[selectcentral]

        if i == 0:
            centralgals = centralchunk
        else:
            centralgals.append(centralchunk, columns=keys)
        
        masstest = np.min(centralchunk[keys[11]])
        i += 1

    halo_sname = halo_name.split('.')
    haloname = halo_sname[0]+'.'+halo_sname[1]
    centralgals.to_csv(userpath+'_'+haloname+'_centralhalos.csv')

    return centralgals
