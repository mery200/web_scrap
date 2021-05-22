import dash
import plotly.express as px
import pandas as pd
import bs4 as bs
import plotly.express as px
from urllib.request import Request, urlopen
import numpy as np
import json
import pandas as pd
import bs4 as bs
import re
import matplotlib.pyplot as plt
import datetime as dt
from urllib.request import Request, urlopen
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import requests
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sklearn.svm import SVR

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# Unpivot data frames
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date2, var_name='date', value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date3, var_name='date', value_name='recovered')

# Merging data frames
covid_data = total_confirmed.merge(right=total_deaths, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right=total_recovered, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

# Converting date column from string to proper date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

# Check how many missing value naN
covid_data.isna().sum()

# Replace naN with 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# Calculate new column
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

# create dictionary of list
covid_data_dict = covid_data[['Country/Region', 'Lat', 'Long']]
list_locations = covid_data_dict.set_index('Country/Region')[['Lat', 'Long']].T.to_dict('dict')


covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == "Morocco"][['Country/Region', 'date', 'confirmed']].reset_index()
covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()

df = covid_data_3.head(len(covid_data_3))
df_p= df.tail(30)
df1= df.tail(483)
df=df1.head(453)
day = list()

adj = list()
df_d1= df_p.loc[:,"date"]
df_d= df.loc[:,"date"]
df_adj = df.loc[:,"daily confirmed"]
for ad in df_adj:
    adj.append(float(ad))

z0=[]
for d in df_d1:
    o = dt.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
    f= dt.datetime.strftime(o, '%Y-%m-%d')
    z0.append([int(f.split('-')[2])])

z=[]
for d in df_d:
    o = dt.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
    f= dt.datetime.strftime(o, '%Y-%m-%d')
    z.append([int(f.split('-')[2])])

lin_svr = SVR(kernel='linear',C=1000.0)
lin_svr.fit(z,adj)

pol_svr = SVR(kernel='poly',C=1000.0, degree=2)
pol_svr.fit(z,adj)

rbf_svr = SVR(kernel='rbf',C=1000.0,gamma=0.85)
rbf_svr.fit(z,adj)




plt.figure(figsize=(16,8))

plt.scatter(z,adj ,color="black",label='data')

z.append([z[len(z)-1][0]+1])
plt.plot(z0,rbf_svr.predict(z0),color="red",label="rbf model")

plt.xlabel('day')
plt.ylabel('confirmed')
plt.show()

ddd=[[17],[18]]
print(rbf_svr.predict(ddd))
