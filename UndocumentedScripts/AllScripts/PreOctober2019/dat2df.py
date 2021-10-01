import pandas as pd
import os

def dat2df(dat_file, delimiter):
    '''
    Converts a dat file to a Pandas data frame

    Parameters
    ----------
    dat_file (str):
        Filepath of dat file
    delimiter (str):
        Delimiter used within each line

    Returns
    -------
    df (pandas.DataFrame):
        Data frame read from dat file
    '''
    f = open(dat_file, 'r')
    first_line = 