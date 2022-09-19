# packages
import numpy as np
import pandas as pd
# raw data
air_raw = pd.read_csv('/Users/nealarashidfarrukhi/Desktop/air-raw.csv')
cbsa_info = pd.read_csv('/Users/nealarashidfarrukhi/Desktop/cbsa-info.csv')

cbsa_info[['Territories','State']]= cbsa_info['Core Based Statistical Area'].str.split(",", expand=True)
cbsa_info.head()
cbsa_new= cbsa_info.drop(columns='Core Based Statistical Area')

data = cbsa_new.merge(air_raw, how = 'right', on = 'CBSA').melt(id_vars=['CBSA','Pollutant','Trend Statistic','Number of Trends Sites','Territories','State'],
                             var_name= 'Year').pivot(index=np.append(cbsa_new.columns,'Year'), columns=['Pollutant','Trend Statistic'],
                                                    values='value').sort_values('Year')
data

# Question 2: How many CBSA's are included in the data?
data.value_counts('CBSA')
# There are 351 CBSA's included in the data every year from 2000-2019

# Question 3: In how many states and territories do the CBSA's reside? (Hint: str.split()) # The CBSA resides in 57 states and territories.
data.reset_index(inplace=True)
data
state = data['State'].str.split('-|',4,expand=True).melt().value.unique().size state

# Question 4: In which years were data values recorded?
data.value_counts('Year', sort=True)
# Data values were recorded from 2000-2019.

# Question 5: How many observations are recorded?
observations=len(data)
observations
# There is a total of 7020 observations recorded in the merged data set.

# Question 6: How many variables are measured?
variable=len(data.columns)
variable
# There are 9 variables that are measured in the merged data set.

data_mod1=data.loc[:,'PM2.5'].groupby('Year').mean()
data_mod1.head(20)
#data_mod1['Weighted Annual Mean']+data_mod1['98th Percentile']
# #Overall PM 2.5 pollution is getting better

#I think what we need is to .loc Pm2.5 and then group by territories and year,and then use the built in variance function but I’m getting just a whole bunch of NaN
data_na=data.dropna(axis=0, how='any')
data_var=data_na.loc[:,'PM2.5'].groupby(['Territories','Year']).var()
data_var

data_mod2=data.loc[:,'PM2.5'].groupby(['State','Year']).mean()
# data_mod2
# loc
data_mod3 = data_mod2.loc[:, ['2000', '2019'], :] data_mod3.diff().loc[:, '2019', :]

data_mod4=data.loc[:,'PM2.5'].groupby(['Territories','Year']).mean()
# data_mod2
# loc
data_mod5 = data_mod4.loc[:, ['2000', '2019'], :] data_mod5.diff().loc[:, '2019', :]

data_mod3=data.loc[:,'PM2.5'].groupby(['Territories','Year']).mean()
data_mod3
data_mod3['Weighted Annual Mean']

# Santa Barbara has had a -5.10 decrease in PM2.5 from 2000 to 2019.
data.reset_index(inplace = True)
data[(data.Territories == 'Santa Maria-Santa Barbara') & (data.Year == '2019')]
