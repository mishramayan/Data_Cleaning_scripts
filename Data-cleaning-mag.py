# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:12:41 2024

@author: Mayan
"""

import os 
import pandas as pd
import numpy as np

df = pd.read_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//SensorData-MagnetometerSensor_OnDesk.csv')

# Convert the timestamp column to datetime
df['Magnetometer.TIMESTAMP{0}'] = pd.to_datetime(df['Magnetometer.TIMESTAMP{0}'])

# Set the timestamp as the index
df.set_index('Magnetometer.TIMESTAMP{0}', inplace=True)

# Define aggregation methods
aggregation = {
    'Magnetometer.X{0} [milliGauss]': 'mean',
    'Magnetometer.Y{0} [milliGauss]': 'mean',
    'Magnetometer.Z{0} [milliGauss]': 'mean',
    'Activity': 'first'
}

# Resample the gyroscope data at 100ms intervals
resampled_mag_df = df.resample('100ms').agg(aggregation)

# Reset index if you prefer the timestamp to be a column again
resampled_mag_df = resampled_mag_df.reset_index()

# Create an index column incrementing by 100
resampled_mag_df['Index'] = range(0, 100 * len(resampled_mag_df), 100)

nulls = resampled_mag_df.isnull().sum()
print("Null values per column:\n", nulls)

# Identify numeric columns for filling missing values
numeric_cols = resampled_mag_df.select_dtypes(include=['float64', 'int64']).columns
non_numeric_cols = resampled_mag_df.select_dtypes(exclude=['float64', 'int64']).columns

# Calculate mean for numeric columns
means = resampled_mag_df[numeric_cols].mean()

# Fill null values in numeric columns with the mean of each column
resampled_mag_df[numeric_cols] = resampled_mag_df[numeric_cols].fillna(means)

# Fill null values in non-numeric columns with the most frequent value (mode)
for col in non_numeric_cols:
    most_frequent_value = resampled_mag_df[col].mode()[0]
    resampled_mag_df[col] = resampled_mag_df[col].fillna(most_frequent_value)
    
nulls = resampled_mag_df.isnull().sum()
print("Null values per column (after):\n", nulls)

resampled_mag_df.to_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//Resampled_Magnetometer_OnDesk.csv', sep=',', index=False, encoding='utf-8')
