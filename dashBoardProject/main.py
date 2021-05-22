import json
import pandas as pd
import bs4 as bs
from urllib.request import Request, urlopen
import dash_core_components as dcc
import dash_html_components as html
import requests
import re
import plotly.graph_objs as go

req = Request('https://www.worldometers.info/coronavirus', headers={'User-Agent': 'Mozilla/5.0'})
source = urlopen(req).read()

# In[2]:

soup = bs.BeautifulSoup(source,"lxml")

table = soup.table

#find the table rows within the table
table_rows = table.find_all('tr')

td_all = []
totals=[]

for tr in table_rows:
    td = tr.find_all('td')
    td_all.append(td)
for k in range(7):
    td_all.pop(0)

country = []
confirmed = []
deaths = []
recovered=[]
population = []
covid_data=[]
globalcase=[]
globaldeath=[]
globalrecover=[]

for i in td_all:
    # print(i[1].text)
    country.append(i[1].text)
    confirmed.append(i[2].text)
    deaths.append(i[4].text)
    recovered.append(i[6].text)
    population.append(i[14].text)

totals.append(country[-1])
globalcase.append(confirmed[-1])
globaldeath.append(deaths[-1])
globalrecover.append(recovered[-1])

#####################################

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
################################################################################

response = requests.get("https://corona.lmao.ninja/v2/continents")
todos = json.loads(response.text)

a=[]
b=[]
c=[]
d=[]
for i in todos:
    a.append(i['continent'])
    b.append(i["cases"])
    c.append(i["recovered"])
    d.append(i["deaths"])


#######################################

req4 = Request('https://apps.npr.org/dailygraphics/graphics/coronavirus-d3-world-map-20200323/continents.html', headers={'User-Agent': 'Mozilla/5.0'})
source4 = urlopen(req4).read()
soup4 = bs.BeautifulSoup(source4,"lxml")
jj = re.search(r'window.ANNOTATIONS\s+=\s+(.*)', str(soup4.find('script', type='text/javascript')), flags=re.DOTALL)
jso= jj[1]

anno = jso.split('\nwindow.DATA = ')
dat = anno[1].split('\nwindow.CONTINENTS')

anno.pop()
dat.pop()

J3 = anno[0].rsplit(';', 1)
J4 = dat[0].rsplit(';', 1)

t= json.loads(J3[0])
k=json.loads(J4[0])

ddd=[]
aaa=[]
c1=[]
c2=[]
c3=[]
c4=[]
c5=[]
c6=[]
for i in k:
    ddd.append(i['date'])
    c1.append(i['Asia'])
    c2.append(i['Europe'])
    c3.append(i['Africa'])
    c4.append(i['North America'])
    c5.append(i['South America'])
    c6.append(i['Oceania'])

############################################################

response3 = requests.get("https://static01.nyt.com/newsgraphics/2021/01/19/world-vaccinations-tracker/49ce342ff11b995136c6e8cd95da52a4698628ef/continent_vaccinations.json")
todos3 = json.loads(response3.text)
yyy=[]
for y in todos3:
    yyy.append(y['total_vaccinations'])

vac=[yyy[3],yyy[1],yyy[5],yyy[2],yyy[0],yyy[4]]
#####################################################################################

response5 = requests.get("https://static01.nyt.com/newsgraphics/2021/01/19/world-vaccinations-tracker/49ce342ff11b995136c6e8cd95da52a4698628ef/latest.json")
todos5 = json.loads(response5.text)
###############################################################################################

dashboard = html.Div([
    dcc.Interval(id='interval1', interval=86400, n_intervals=0),
    # html.Div([
    #     html.Img(src=app.get_asset_url('coronas.png'),
    #              id='corona-image',
    #              style={
    #                  "height":"100px",
    #                  "width":"auto",
    #                  "margin-bottom":"25px",
    #              }
    #              )
    # ],
    # className='one-third column'
    # ),
    html.Header([
        html.Div([
            html.H4("Pandemic DashBord", style={"margin-top": "0px", 'color': 'black'}),
        ])
    ],  id="title"),
    html.Div([
        html.Div([
    html.Div([
        html.Div([
            html.H6(children='Global Confirmed Cases',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P(f"{globalcase[0]:}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 30}
                   ),
        ])
    ],className="card_container three columns",),

    html.Div([
        html.Div([
            html.H6(children='Global Deaths',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P(f"{globaldeath[0]:}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 30}
                   ),

        ])
    ], className="card_container three columns",),
    html.Div([
        html.Div([
            html.H6(children='Global Recovered',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{globalrecover[0]:}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 30}
                   ),
        ])
    ],className="card_container three columns",),
html.Div([
        html.Div([
            html.H6(children='Global Vaccinations',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P(f"{'{:,}'.format(sum(vac)):}",
                   style={
                       'textAlign': 'center',
                       'color': '#F3DAAC',
                       'fontSize': 30}
                   ),

        ])
    ], className="card_container two columns", style={'width': '6.7cm'}),
],className="row"),
html.Div(children=[
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [go.Bar(x=a,
                        y=b,
                        name='Confirmed cases',
                        marker=dict(
                        color='orange'),
                        hoverinfo='x+y',
                 ),go.Bar(x=a,
                        y=c,

                        name='Recovers',
                        marker=dict(
                            color='green'),
                        hoverinfo='x+y',
                ),go.Bar(x=a,
                        y=d,

                        name='Deaths',
                        marker=dict(
                            color='red'),
                        hoverinfo='x+y',
                ),go.Bar(x=a,
                        y=vac,

                        name='Vaccination',
                        marker=dict(
                            color='#F3DAAC'),
                        hoverinfo='x+y',
                          )],
            'layout':
            go.Layout(title='Comparison between the pandemic evolution & the number of vaccination by continent', plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b>continents</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )
             ),legend={
                'orientation': 'h',
                'bgcolor': '#283179',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),
        )})
]),
html.Div(children=[
    dcc.Graph(
        id='graph2',
        figure={
            'data': [go.Scatter(x=ddd, y=c5, fill='tozeroy',name='South America',
                    mode='lines' # override default markers+lines
                    ),go.Scatter(x=ddd, y=c4, fill='tozeroy',name='North America',
                    mode= 'lines'),
                    go.Scatter(x=ddd, y=c3, fill='tozeroy',name='Africa',
                    mode= 'lines'),
                     go.Scatter(x=ddd, y=c2, fill='tozeroy', name='Europe',
                    mode='lines'),
                    go.Scatter(x=ddd, y=c1, fill='tozeroy',name='Asia',
                    mode= 'lines'),
                    go.Scatter(x=ddd, y=c6, fill='tozeroy',name='Oceania',
                    mode= 'lines')
                     ],
            'layout':
            go.Layout(title='pandemic cases evolution by continent',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b>continents</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )
             ),legend={
                'orientation': 'h',
                'bgcolor': '#283179',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),
        )})
]),

        #----------------charts--------------------
html.Div([
        html.Div([

                    html.P('Select Country:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='w_countries',
                                  multi=False,
                                  clearable=True,
                                  value='Morocco',
                                  placeholder='Select Countries',
                                  options=[{'label': c, 'value': c}
                                           for c in (covid_data['Country/Region'].unique())], className='dcc_compon'),

                     html.P('New Cases : ' + '  ' + ' ' + str(covid_data_2['date'].iloc[-1].strftime("%B %d, %Y")) + '  ', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
                     dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'},
                     ),

                      dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

        ], className="create_container three columns", id="cross-filter-options"),
            html.Div([
                      dcc.Graph(id='pie_chart',
                              config={'displayModeBar': 'hover'}),
                              ], className="create_container four columns"),

                    html.Div([
                        dcc.Graph(id="line_chart")

                    ], className="create_container four columns"),

        ], className="row"),

html.Div([
        html.Div([
            dcc.Graph(id="map")], className="create_container1 twelve columns"),

            ], className="row flex-display"),

], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})
])




req = Request('https://www.worldometers.info/coronavirus', headers={'User-Agent': 'Mozilla/5.0'})
source = urlopen(req).read()

# In[2]:

soup = bs.BeautifulSoup(source,"lxml")

table = soup.table

#find the table rows within the table
table_rows = table.find_all('tr')

td_all = []

for tr in table_rows:
    td = tr.find_all('td')
    td_all.append(td)
for k in range(7):
    td_all.pop(0)

country = []
cases = []
population = []
deaths = []
recovred = []

for i in td_all:
    #print(i[1].text)
    country.append(i[1].text)
    cases.append(i[2].text)
    population.append(i[14].text)
    deaths.append(i[4].text)
    recovred.append(i[6].text)
for t in range(8):
    country.pop()
    cases.pop()
    deaths.pop()
    recovred.pop()

import csv
c = []
with open('covid_data.csv', 'a+', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    col = ['country', 'cases', 'deaths', 'recovres']
    spamwriter.writerow("\n")
    spamwriter.writerow(country)
    spamwriter.writerow(cases)
    spamwriter.writerow(deaths)
    spamwriter.writerow(recovred)
