import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

averages_filepath = "/Users/samdhanani/Desktop/MuhleLab/Operant_Data_Folders/burst_file.csv"  
averages_df = pd.read_csv(averages_filepath)

# List of columns to calculate averages for
columns_to_average = ['number of bursts', 'sum of all bursts', 'average burst time','average_burst_press_count']

for column in columns_to_average:
    if averages_df[column].dtype == 'object':
        averages_df[column] = averages_df[column].str.replace(r'[^0-9.]', '', regex=True)
        averages_df[column] = pd.to_numeric(averages_df[column], errors='coerce')

averages_df['Program'] = averages_df['Program'].str.extract('(\d+)')
averages_df['Program'] = pd.to_numeric(averages_df['Program'], errors='coerce')

grouped_averages_df = averages_df.groupby(['Program', 'Subject', 'Genotype', 'Sex'])[
    columns_to_average + ['Date']
].agg({'Date': 'first', **{col: 'mean' for col in columns_to_average}}).reset_index()

csv_filepath = "/Users/samdhanani/Desktop/MuhleLab/Operant_Data_Folders/CohF_DRH_AVGburst2-3s_030724.csv"

grouped_averages_df.to_csv(csv_filepath, index=False)

print(grouped_averages_df)
