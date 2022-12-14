import pandas as pd
import numpy as np
import altair as alt

ncca_raw = pd.read_csv('/home/jovyan/pstat100-content/project/mp2/assessed_ncca2010_waterchem.csv')
ncca_sites = pd.read_csv('/home/jovyan/pstat100-content/project/mp2/assessed_ncca2010_siteinfo.csv')

# First I am going to create seperate columns for Chlorophyll A, Total Nitrogen and Total Phosphorus
# Select columns and rows we want in new data frame

ncca_loc = ncca_raw.loc[
    (ncca_raw['PARAMETER_NAME'] == 'Total Nitrogen') | (ncca_raw['PARAMETER_NAME'] == 'Total Phosphorus') |
    (ncca_raw['PARAMETER_NAME'] == 'Chlorophyll A')].drop(columns=['METHOD', 'QACODE', 'PQL'])
ncca_loc

# pivot to make rows into columns with results as the value

ncca_new_raw = ncca_loc.pivot(index='UID', columns='PARAMETER_NAME', values='RESULT')
# print head
ncca_new_raw.head(20)

# I am selecting all the columns I want in my data
all_data = ncca_new_raw.merge(ncca_sites, on='UID', how='right')
data_clean = all_data[['Chlorophyll A', 'Total Nitrogen', 'Total Phosphorus', 'STATE', 'WTBDY_NM', 'WGT_NCCA10',
                       'ALAT_DD', 'ALON_DD', 'NCCR_REG', 'DATE_COL', 'STATION_DEPTH', 'NCA_REGION']]
data_clean

# In order to add seasons I will be using string split to pars the data
data_clean_1 = data_clean['DATE_COL'].str.split("-", expand=True)
data_clean['Seasons'] = data_clean_1[1]
data_clean

# I want to rename all the months from numeric to their real names
Final_Data = data_clean.loc[data_clean['Seasons'].isin(['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'])]
Final_Data.head(10)

Nitro_Graph = alt.Chart(ncca_new_raw).mark_circle(opacity=0.5).encode(
    x=alt.X('Total Nitrogen', scale=alt.Scale(type='log')),
    y=alt.Y('Chlorophyll A', title='Chlorophyll A', scale=alt.Scale(type='sqrt')))
# scale properly so data is proper for analyzing

Phos_Graph = alt.Chart(ncca_new_raw).mark_circle(opacity=0.5).encode(
    x=alt.X('Total Phosphorus', scale=alt.Scale(type='sqrt')),
    y=alt.Y('Chlorophyll A', title='Chlorophyll A', scale=alt.Scale(type='sqrt')))
# scale properly so data is proper for analyzing

display(Nitro_Graph)
display(Phos_Graph)

scatter = alt.Chart(ncca_new_raw_1).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Nitrogen', scale=alt.Scale(type='sqrt')),
    y=alt.Y('Chlorophyll A', title='Chlorophyll A', scale=alt.Scale(type='sqrt')),
    color='NCA_REGION')

smooth = scatter.transform_loess(
    groupby=['NCA_REGION'],
    on='Total Nitrogen',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_1 = scatter + smooth
scatter = alt.Chart(ncca_new_raw_1).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Phosphorus', scale=alt.Scale(type='sqrt')),
    y=alt.Y('Chlorophyll A', title='Chlorophyll A', scale=alt.Scale(type='sqrt')),
            color='NCA_REGION')

smooth=scatter.transform_loess(
    groupby=['NCA_REGION'],
    on='Total Phosphorus',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_2 = scatter + smooth
display(Graph_1)
display(Graph_2)

# Create an interactive map to see clearly
points = alt.Chart(data_clean).mark_circle(
    color="purple"
).encode(
    x="ALON_DD:Q", y="ALAT_DD:Q", size="Chlorophyll A:Q",
    tooltip=["WTBDY_NM", "Chlorophyll A"]
).interactive()

points

# histogram to further analyze the data based on region
alt.Chart(ncca_new_raw_2).transform_filter(
    alt.FieldOneOfPredicate(field='NCCR_REG',
                            oneOf=['West', 'Southeast', 'Great Lakes', 'Gulf', 'Northeast', ])
).mark_bar(opacity=0.5).encode(
    x=alt.X('Chlorophyll A', scale=alt.Scale(type='sqrt'), bin=alt.Bin(step=2),
            title='Histogram of Chlorophyl in Different Regions'),
    y=alt.Y('count()', stack=None),
    color='NCCR_REG'
)

data_clean_chart = data_clean.loc[data_clean['Seasons'].isin(['May', 'Jun', 'Jul', 'Aug'])]
data_clean_chart

scatter = alt.Chart(data_clean_chart).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Nitrogen', scale=alt.Scale(type='log')),
    y=alt.Y('Chlorophyll A', scale=alt.Scale(type='sqrt')),
    color='Seasons'
title = 'Summer')

smooth = scatter.transform_loess(
    groupby=['Seasons'],
    on='Total Nitrogen',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_N = scatter + smooth

scatter = alt.Chart(data_clean_chart).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Phosphorus'),
    y=alt.Y('Chlorophyll A'),
    color='Seasons'
).properties(
    title='Summer')

smooth = scatter.transform_loess(
    groupby=['Seasons'],
    on='Total Phosphorus',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_T = scatter + smooth
display(Graph_N)
display(Graph_T)

data_clean_chart2 = data_clean.loc[data_clean['Seasons'].isin(['Sep', 'Oct'])]
data_clean_chart2

scatter = alt.Chart(data_clean_chart2).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Nitrogen', scale=alt.Scale(type='log')),
    y=alt.Y('Chlorophyll A', scale=alt.Scale(type='sqrt')),
    color='Seasons'
).properties(
    title='Autumn')

smooth = scatter.transform_loess(
    groupby=['Seasons'],
    on='Total Nitrogen',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_Fall_1 = scatter + smooth

scatter = alt.Chart(data_clean_chart2).mark_circle(opacity=0.75).encode(
    x=alt.X('Total Phosphorus'),
    y=alt.Y('Chlorophyll A'),
    color='Seasons'
).properties(
    title='Autumn')

smooth = scatter.transform_loess(
    groupby=['Seasons'],
    on='Total Phosphorus',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_Fall_2 = scatter + smooth
display(Graph_Fall_1)
display(Graph_Fall_2)

scatter = alt.Chart(Final_Data).mark_circle(opacity=0.75).encode(
    x=alt.X('STATION_DEPTH', scale=alt.Scale(type='sqrt')),
    y=alt.Y('Chlorophyll A', scale=alt.Scale(type='sqrt')),
    color='Seasons'
).properties(
    title='Summer')

smooth = scatter.transform_loess(
    groupby=['Seasons'],
    on='STATION_DEPTH',  # x variable
    loess='Chlorophyll A',  # y variable
    bandwidth=0.25  # how smooth?
).mark_line(color='black')

Graph_S = scatter + smooth
display(Graph_S)