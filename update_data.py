import os

import pyspedas
import pandas as pd

def main():
    noaa_update()

def noaa_update():
    '''
    This function checks if the NOAA Kp index and OMNI data files exist.
    If they do not exist, it downloads the data using the pyspedas library and saves them as CSV files.
    '''

    start_date = '2023-05-14/00:00:00'
    end_date = '2024-05-14/23:59:59'

    #check if there is a 'noaa_kp.csv' in the '/data' folder
    
    if not os.path.exists('noaa_kp.csv'):
        print("noaa_kp.csv not found in /data folder.")
        vars = pyspedas.projects.noaa.noaa_load_kp(trange=[start_date, end_date], local_kp_dir=None, datatype=[], gfz=False, prefix='', suffix='', time_clip=True, force_download=False)
        
        parts = {}
        for name in vars:
            d = pyspedas.get_data(name)
            parts[name] = pd.Series(d.y, index=pd.to_datetime(d.times, unit='s'))
                    
            df_kp = pd.concat(parts, axis=1)  # one column per variable, aligned on time
            df_kp.to_csv('noaa_kp.csv', index=True)
        
    else:
        print("noaa_kp.csv found in /data folder")

        
    #check if there's a 'omni_data.csv' in the '/data' folder
    if not os.path.exists('omni_data.csv'):
        print("omni_data.csv not found in /data folder")

        wind_data = pyspedas.projects.omni.data(
        trange=[start_date, end_date],    
        datatype='1min',
        )
        parts = {}
        for name in wind_data:
            d = pyspedas.get_data(name)
            parts[name] = pd.Series(d.y, index=pd.to_datetime(d.times, unit='s'))
            
        df_omni = pd.concat(parts, axis=1)  # one column per variable, aligned on time
        df_omni.to_csv('omni_data.csv', index=True)
    else:
        print("omni_data.csv found in /data folder. ")

    #check if there's a 'dscovr_data.csv' in the '/data' folder
    if not os.path.exists('dscovr_data.csv'):
        print("dscovr_data.csv not found in /data folder")

        dscovr_data = pyspedas.projects.dscovr.mag(
        trange=[start_date, end_date],    
        instrument=['mag', 'faraday_cup'],
        )
        parts = {}

        for name in dscovr_data:
            d = pyspedas.get_data(name)

            index = pd.to_datetime(d.times, unit='s')

            if d.y.ndim == 2:
            # Create separate columns for each magnetic field component
                columns = [f'{name}_{component}' for component in ['Bx', 'By', 'Bz']]

                parts[name] = pd.DataFrame(
                d.y,
                index=index,
                columns=columns
                )
            else:
                parts[name] = pd.Series(
                d.y,
                index=index,
                name=name
        )

        df_dscovr = pd.concat(parts.values(), axis=1)
        df_dscovr.to_csv('dscovr_data.csv', index=True)
    else:
        print("dscovr_data.csv found in /data folder.")

if __name__ == "__main__":
    main()