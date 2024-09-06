# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:07:35 2024

@author: Mayan
"""

import os 
import pandas as pd
import numpy as np

df = pd.read_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//SensorData-Gyro_OnDesk.csv')

# Convert the timestamp column to datetime
df['Gyroscope.TIMESTAMP{0}'] = pd.to_datetime(df['Gyroscope.TIMESTAMP{0}'])

# Set the timestamp as the index
df.set_index('Gyroscope.TIMESTAMP{0}', inplace=True)

# Define aggregation methods
aggregation = {
    'Gyroscope.AngularVelocityX{0}': 'mean',
    'Gyroscope.AngularVelocityY{0}': 'mean',
    'Gyroscope.AngularVelocityZ{0}': 'mean',
    'Activity': 'first'
}

# Resample the gyroscope data at 100ms intervals
resampled_gyro_df = df.resample('100ms').agg(aggregation)

# Reset index if you prefer the timestamp to be a column again
resampled_gyro_df = resampled_gyro_df.reset_index()

# Create an index column incrementing by 100
resampled_gyro_df['Index'] = range(0, 100 * len(resampled_gyro_df), 100)


nulls = resampled_gyro_df.isnull().sum()
print("Null values per column:\n", nulls)


# Identify numeric columns for filling missing values
numeric_cols = resampled_gyro_df.select_dtypes(include=['float64', 'int64']).columns
non_numeric_cols = resampled_gyro_df.select_dtypes(exclude=['float64', 'int64']).columns

# Calculate mean for numeric columns
means = resampled_gyro_df[numeric_cols].mean()

# Fill null values in numeric columns with the mean of each column
resampled_gyro_df[numeric_cols] = resampled_gyro_df[numeric_cols].fillna(means)

# Fill null values in non-numeric columns with the most frequent value (mode)
for col in non_numeric_cols:
    most_frequent_value = resampled_gyro_df[col].mode()[0]
    resampled_gyro_df[col] = resampled_gyro_df[col].fillna(most_frequent_value)

    
nulls = resampled_gyro_df.isnull().sum()
print("Null values per column (after):\n", nulls)

resampled_gyro_df.to_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//Resampled_Gyro_OnDesk.csv', sep=',', index=False, encoding='utf-8')
