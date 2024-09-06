# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:32:33 2024

@author: Mayan
"""
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//SensorData-Accelerometer_OnDesk.csv')


# Convert TIMESTAMP to datetime
df['Accelerometer.TIMESTAMP{0}'] = pd.to_datetime(df['Accelerometer.TIMESTAMP{0}'])

# Set as index
df.set_index('Accelerometer.TIMESTAMP{0}', inplace=True)

# Define aggregation
aggregation = {
    'Accelerometer.AccelerationX{0}': 'mean',
    'Accelerometer.AccelerationY{0}': 'mean',
    'Accelerometer.AccelerationZ{0}': 'mean',
    'Accelerometer.Shake{0}': 'first',
    'Activity': 'first'
}

# Resample at 100ms
resampled_df = df.resample('100ms').agg(aggregation).reset_index()

# Create an index column incrementing by 100
resampled_df['Index'] = range(0, 100 * len(resampled_df), 100)

nulls = resampled_df.isnull().sum()
print("Null values per column:\n", nulls)


# Identify numeric columns for filling missing values
numeric_cols = resampled_df.select_dtypes(include=['float64', 'int64']).columns
non_numeric_cols = resampled_df.select_dtypes(exclude=['float64', 'int64']).columns

# Calculate mean for numeric columns
means = resampled_df[numeric_cols].mean()

# Fill null values in numeric columns with the mean of each column
resampled_df[numeric_cols] = resampled_df[numeric_cols].fillna(means)

# Fill null values in non-numeric columns with the most frequent value (mode)
for col in non_numeric_cols:
    most_frequent_value = resampled_df[col].mode()[0]
    resampled_df[col] = resampled_df[col].fillna(most_frequent_value)

    
nulls = resampled_df.isnull().sum()
print("Null values per column (after):\n", nulls)

resampled_df.to_csv('C://Users//Srinath//Desktop//HAR Data copy//On Desk//Resampled_Accelerometer_OnDesk.csv', sep=',', index=False, encoding='utf-8')

print(resampled_df)