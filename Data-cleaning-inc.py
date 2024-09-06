# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 12:38:01 2024

@author: Mayan
"""

import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//SensorData-Inclinometer_OnDesk.csv')


# Convert the timestamp column to datetime
df['Inclinometer.TIMESTAMP{0}'] = pd.to_datetime(df['Inclinometer.TIMESTAMP{0}'])

# Set the timestamp as the index
df.set_index('Inclinometer.TIMESTAMP{0}', inplace=True)

# Define aggregation methods
aggregation = {
    'Inclinometer.PitchDegrees{0}': 'mean',
    'Inclinometer.RollDegrees{0}': 'mean',
    'Inclinometer.YawDegrees{0}': 'mean',
    'Inclinometer.QuaternionW{0}': 'mean',
    'Inclinometer.QuaternionX{0}': 'mean',
    'Inclinometer.QuaternionY{0}': 'mean',
    'Inclinometer.QuaternionZ{0}': 'mean',
    'Activity': 'first'
}

# Resample the inclinometer data at 100ms intervals
resampled_incl_df = df.resample('100ms').agg(aggregation)

# Reset index if you prefer the timestamp to be a column again
resampled_incl_df = resampled_incl_df.reset_index()

# Forward fill the activity column
resampled_incl_df['Activity'] = resampled_incl_df['Activity'].ffill()

# Interpolate missing numeric values
resampled_incl_df[['Inclinometer.PitchDegrees{0}', 
                   'Inclinometer.RollDegrees{0}', 
                   'Inclinometer.YawDegrees{0}', 
                   'Inclinometer.QuaternionW{0}', 
                   'Inclinometer.QuaternionX{0}', 
                   'Inclinometer.QuaternionY{0}', 
                   'Inclinometer.QuaternionZ{0}']] = resampled_incl_df[['Inclinometer.PitchDegrees{0}', 
                                                                         'Inclinometer.RollDegrees{0}', 
                                                                         'Inclinometer.YawDegrees{0}', 
                                                                         'Inclinometer.QuaternionW{0}', 
                                                                         'Inclinometer.QuaternionX{0}', 
                                                                         'Inclinometer.QuaternionY{0}', 
                                                                         'Inclinometer.QuaternionZ{0}']].interpolate(method='linear')
# Create an index column incrementing by 100
resampled_incl_df['Index'] = range(0, 100 * len(resampled_incl_df), 100)

nulls = resampled_incl_df.isnull().sum()
print("Null values per column:\n", nulls)

resampled_incl_df.to_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//Resampled_Inclinometer_OnDesk.csv', sep=',', index=False, encoding='utf-8')

print(resampled_incl_df)





