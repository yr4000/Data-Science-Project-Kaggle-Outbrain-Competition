from paths import *
import numpy as np
import pandas as pd
from utils.table_utils import filter_table_by_unique_ids, return_unique_values_of_column_from_table

#returns the countries from display_geo who which are at list 1% from all the countries appears
def filter_countries_by_size(disp_geo,size):
    countries = disp_geo.groupby(["country"], as_index=False).agg({"display_id": np.count_nonzero})\
        .rename(index=str, columns={"display_id" : 'country_count'})[1:]
    countries = countries[countries['country_count']>len(disp_geo)/size]
    return countries

def create_binary_country_vectors(main_table):
    countries = main_table["geo_location"]
    country_is_US = np.array(countries == 'US', dtype=int)
    country_is_GB = np.array(countries == 'GB', dtype=int)
    country_is_CA = np.array(countries == 'CA', dtype=int)
    country_is_AU = np.array(countries == 'AU', dtype=int)

    # Creating the result Dataframe
    res_frame = pd.DataFrame()
    res_frame["country_is_US"] = country_is_US
    res_frame["country_is_GB"] = country_is_GB
    res_frame["country_is_CA"] = country_is_CA
    res_frame["country_is_AU"] = country_is_AU

    return res_frame

def count_states(disp_geo):
    states = disp_geo[['state']]
    state_count = states.groupby("state").state.agg("count")
    state_count = pd.Series(state_count.as_matrix())

    # Extracting vector of unique states
    states = states["state"].unique()

    # Creating result Dataframe, contaning the state count
    # for each unique display
    res_frame = pd.DataFrame()
    res_frame["state"] = states
    res_frame["state_count"] = state_count.astype(int)
    return res_frame

def create_count_state(main_table,disp_geo):
    unique_displays = return_unique_values_of_column_from_table('display_id',main_table)
    relavent_states = filter_table_by_unique_ids(unique_displays,"display_id",DISPLAY_GEO_YAIR)
    count_state_frame = count_states(disp_geo)
    res_frame = relavent_states.merge(count_state_frame,on='state')
    res_frame = res_frame.dropna()
    res_frame = res_frame[res_frame.state != '--']
    res_frame.drop(['country','state','DMA'], axis=1, inplace=True)
    return res_frame

