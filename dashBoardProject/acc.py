import csv
import json
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import requests
from dash.dependencies import Input, Output
import datetime as dt
from sklearn.svm import SVR
import datetime
import predict
import main


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


navbar = html.Header([
dbc.NavbarSimple(

    [           dbc.NavLink("About Covid-19", href="/", active="exact"),
                dbc.NavLink("Dashboard", href="/dash", active="exact"),
                dbc.NavLink("Prediction", href="/prediction", active="exact"),

    ],
    brand="Covid-19",
    brand_href="/",
    color="#283179",
    dark=True,
    style={'textAlign': 'center'},
)
],className='navbar-custom fluid')



# section = html.Div([
#     html.H1(
#         "CORONAVIRUS"
#     ,style={"textColor":'white'})
#
# ],style={'backgroundColor':'#242C6D', 'height': '300px', 'backgroundImage':app.get_asset_url("corona.png")
#          })
# # # # 'backgroundImage':"url('images/illustrations/corona.png')"


container1 = html.Div([
html.Br(),
    dbc.Row([
        html.Div([
            dbc.CardDeck([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Covid-19", className="card-title"),
                        html.P(
                        "COVID-19 is an illness that can affect your lungs and airways. "
                        "It's caused by a virus called coronavirus. It was discovered in December 2019 in Wuhan, Hubei, China. "
                        "Common signs of infection include respiratory symptoms,fever,cough,shortness of breath and breathing difficulties. "
                        "In more severe cases, "
                        "infection can cause pneumonia, severe acute respiratory syndrome, kidney failure and even death.",
                        className="card-text",
                    ),

                    ],style={'textAlign':'center'})
                ]),
                dbc.Card([
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                        dbc.Col([
                    dbc.Card([
                        dbc.Progress(value=98,striped=True,animated=True,color="danger"),
                        html.H5("Fever", className="card-footer"),
                        html.H6("98%"),

                    ]),
                        ],lg=6),
                        dbc.Col([
                 dbc.Card([
                        dbc.Progress(value=76,striped=True,animated=True,color="warning"),
                        html.H5("Cough", className="card-footer"),
                        html.H6("75%"),

                    ]),
],lg=6),
                            ]),
                        dbc.Row([
                            dbc.Col([
                 dbc.Card([
                        dbc.Progress(value=45,striped=True,animated=True,color="success"),
                        html.H5("Pain", className="card-footer"),
                        html.H6("45%"),

                    ]),
],lg=6),
                            dbc.Col([
                 dbc.Card([
                        dbc.Progress(value=15,striped=True,animated=True,color="primary"),
                        html.H5("Diarreah", className="card-footer"),
                        html.H6("15%"),

                    ]),
],lg=6),
                        ])

                    ],style={'textAlign':'center'}),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Symptoms In Most Cases", className="card-title"),
                        html.Img(src=app.get_asset_url("symptoms.png"),width="90%"),
                    ],style={'textAlign':'center'})
                ]),

            ])
        ])
    ])

],className='container-fluid',style={'padding':'2px'})
container2 = html.Div([
    html.Br(),
    dbc.Row([
        html.Div([
            html.H5("How Does The Virus Transmet?",className='my-4 ',style={'textAlign':'center'}),
            dbc.CardDeck([
                dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("spread.png"), top=True, style={'width':'242px','height':'142px'}),
                    dbc.CardBody([
                        html.H4("Direct Contact with Infected person", className='card-title'),
                        html.P("The coronavirus is thought to spread mainly from person to person. "
                               "This can happen between people who are in close contact.")

                    ])
                ],style={'textAlign':'center', 'backgroundColor':'#483D8B'}),
                dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("surface.png"), top=True,
                                style={'width': '242px', 'height': '142px'}),
                    dbc.CardBody([
                        html.H4("Touching infected Surfaces or Objects", className='card-title'),
                        html.P("A person can get COVID-19 by touching a surface or object that has the virus on it "
                               "and then touching their own mouth, nose, or possibly their eyes.",className='card-text')

                    ])
                ], style={'textAlign': 'center', 'backgroundColor': '#483D8B'}),
                dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("cough.png"), top=True,
                                style={'width': '242px', 'height': '142px'}),
                    dbc.CardBody([
                        html.H4("Droplets from infected person's coughs or sneezes", className='card-title'),
                        html.P("The coronavirus is thought to spread mainly from person to person. "
                               "This can happen between people who are in close contact.",className='card-text',style={'color':'white'})

                    ])
                ], style={'textAlign': 'center', 'backgroundColor': '#483D8B'}),

            ],style={'color':'white'})
        ],className='col-12')
    ])

],className='container-fluid')
container3 = html.Div([
    html.Br(),
    dbc.Row([
        html.Div([
            html.H5("Better Safe Than Sorry, Protect Yourself!",className='my-4 ',style={'textAlign':'center'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Wear a mask.Save lives.",className='card-title'),
                            html.Ul([
                                # html.I(className='fas fa-check'),
                                # html.I(fa.icons['check']),
                                html.Li([
                                    "Clean your hands often. Use soap and water, "
                                    "or an alcohol-based hand rub."
                                         ]),
html.Li([
                                    "Maintain a safe distance from anyone who is coughing or sneezing."
                                         ]),
html.Li([
                                    "Don’t touch your eyes, nose or mouth."
                                         ]),
html.Li([
                                    "Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze."
                                         ]),
html.Li([
                                    "Wear a mask when physical distancing is not possible."
                                         ]),
html.Li([
                                    "Stay home if you feel unwell."
                                         ]),
html.Li([
                                    "If you have a fever, cough and difficulty breathing, seek medical attention."
                                         ]),



                            ]),
                            html.P("Calling in advance allows your healthcare provider to quickly direct you to the right health "
                                   "facility. This protects you, and prevents the spread of viruses and other infections.",className='card-text')

                        ],style={'textAlign':'center'})
                    ])
                ],md=7),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Img(src=app.get_asset_url("fight.png"), style={'width': '253px', "height": '330px'})
                        ],style={'textAlign':'center'})
                    ])
                ],md=5,style={'textAlign':'center'}),
            ])
        ],className='col-12')
])
    ])

about = html.Div([
    container1,
    container2,
    container3
])

content = html.Div(id="page-content", children=[])

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    content
    # section,
    # container1,
    # container2,
    # container3

])

####################################dash#########################################
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


response3 = requests.get("https://static01.nyt.com/newsgraphics/2021/01/19/world-vaccinations-tracker/49ce342ff11b995136c6e8cd95da52a4698628ef/continent_vaccinations.json")
todos3 = json.loads(response3.text)
yyy=[]
for y in todos3:
    yyy.append(y['total_vaccinations'])

vac=[yyy[3],yyy[1],yyy[5],yyy[2],yyy[0],yyy[4]]


response5 = requests.get("https://static01.nyt.com/newsgraphics/2021/01/19/world-vaccinations-tracker/49ce342ff11b995136c6e8cd95da52a4698628ef/latest.json")
todos5 = json.loads(response5.text)
#----------------------------------------------------------------------------


@app.callback(
    Output('confirmed', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_confirmed,
                    delta={'reference': delta_confirmed,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Confirmed',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='orange'),
                paper_bgcolor='#283179',
                plot_bgcolor='#283179',
                height=50
                ),

            }

@app.callback(
    Output('death', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_death,
                    delta={'reference': delta_death,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Death',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#dd1e35'),
                paper_bgcolor='#283179',
                plot_bgcolor='#283179',
                height=50
                ),

            }

@app.callback(
    Output('recovered', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_recovered,
                    delta={'reference': delta_recovered,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Recovered',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='green'),
                paper_bgcolor='#283179',
                plot_bgcolor='#283179',
                height=50
                ),

            }

@app.callback(
    Output('active', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_active,
                    delta={'reference': delta_active,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Active',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#e55467'),
                paper_bgcolor='#283179',
                plot_bgcolor='#283179',
                height=50
                ),

            }

# Create pie chart (total casualties)
@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries', 'value')])

def update_graph(w_countries):
    #print(w_countries+"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    new_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    new_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1]
    new_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    new_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    for t in todos5:
        if( t['location']==w_countries):
            new_vac=t['total_vaccinations']
    colors = ['orange', '#dd1e35', 'green', '#e55467','#F3DAAC']

    return {
        'data': [go.Pie(labels=['Confirmed', 'Death', 'Recovered', 'Active','Vaccination'],
                        values=[new_confirmed, new_death, new_recovered, new_active,new_vac],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                        # insidetextorientation='radial',


                        )],

        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor='#283179',
            paper_bgcolor='#283179',
            hovermode='closest',
            title={
                'text': '',


                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
            ),


        }

# Create bar chart (show new cases)
@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# main data frame
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
# daily confirmed
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()

    return {
        'data': [go.Bar(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
                        y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily confirmed'].tail(30),

                        name='Daily confirmed',
                        marker=dict(
                            color='orange'),
                        hoverinfo='text',
                        hovertext=
                        '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
                        '<b>Daily confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily confirmed'].tail(30)] + '<br>' +
                        '<b>Country</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['Country/Region'].tail(30).astype(str) + '<br>'


                        ),
                 go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
                            y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30),
                            mode='lines',
                            name='Rolling average of the last seven days - daily confirmed cases',
                            line=dict(width=3, color='#FF00FF'),
                            # marker=dict(
                            #     color='green'),
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
                            '<b>Rolling Ave.(last 7 days)</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30)] + '<br>'
                            )],


        'layout': go.Layout(
             plot_bgcolor='#283179',
             paper_bgcolor='#283179',
             title={
                'text': 'Last 30 Days Confirmed Cases : ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 20},

             hovermode='x',
             margin = dict(r = 0),
             xaxis=dict(title='<b>Date</b>',
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

             yaxis=dict(title='<b>Daily confirmed Cases</b>',
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

            legend={
                'orientation': 'h',
                'bgcolor': '#283179',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),

                 )

    }

# Create scattermapbox chart
@app.callback(Output('map', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
    covid_data_3 = covid_data.groupby(['Lat', 'Long', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].max().reset_index()
    covid_data_4 = covid_data_3[covid_data_3['Country/Region'] == w_countries]
    for w in todos5:
        if( w['location']==w_countries):
            new_vac=w['total_vaccinations']
    if w_countries:
        zoom = 2
        zoom_lat = list_locations[w_countries]['Lat']
        zoom_lon = list_locations[w_countries]['Long']

    return {
        'data': [go.Scattermapbox(
                         lon=covid_data_4['Long'],
                         lat=covid_data_4['Lat'],
                         mode='markers',
                         marker=go.scattermapbox.Marker(
                                  size=covid_data_4['confirmed'] / 1500,
                                  color=covid_data_4['confirmed'],
                                  colorscale='hsv',
                                  showscale=False,
                                  sizemode='area',
                                  opacity=0.3),

                         hoverinfo='text',
                         hovertext=
                         '<b>Country</b>: ' + covid_data_4['Country/Region'].astype(str) + '<br>' +
                         '<b>Longitude</b>: ' + covid_data_4['Long'].astype(str) + '<br>' +
                         '<b>Latitude</b>: ' + covid_data_4['Lat'].astype(str) + '<br>' +
                         '<b>Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_4['confirmed']] + '<br>' +
                         '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_4['death']] + '<br>' +
                         '<b>Recovered</b>: ' + [f'{x:,.0f}' for x in covid_data_4['recovered']] + '<br>' +
                         '<b>Active</b>: ' + [f'{x:,.0f}' for x in covid_data_4['active']] + '<br>'+
                         '<b>vaccination</b>:' + [f'{"{:,}".format(new_vac)}']+'<br>'
                        )],


        'layout': go.Layout(
             margin={"r": 0, "t": 0, "l": 0, "b": 0},
             # width=1820,
             # height=650,
             hovermode='closest',
             mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_lon),
                # style='open-street-map',
                style='dark',
                zoom=zoom
             ),
             autosize=True,

        )

    }

#########################################predict######################################


#-----------------------------------------------------------------------------------------

@app.callback(Output('id1', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[3]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Life expectancy at birth',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

@app.callback(Output('id2', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[2]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Poverty headcount ratio at national poverty (%)',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

@app.callback(Output('id3', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[8]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Literacy rate, adult',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

@app.callback(Output('id4', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[7]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Death rate',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

@app.callback(Output('id5', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[1]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Population growth',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

@app.callback(Output('id6', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
    Names = []
    Names.append(cc)
    with open(
            "C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv",
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row["ï»¿Country Name"] in Names]

    v = []
    for k in rows:
        dct = k
        v.append(list(dct.items()))

    w = v[9]
    z = []
    y = []
    for t in w[4:]:
        y.append(t[0])
        z.append(t[1])

    return {
        'data': [go.Scatter(
                    x=y,
                    y=z,
                    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
                    connectgaps=True # override default to connect the gaps
                    )],
            'layout':
            go.Layout(title='Gross domestic savings (current US$)',plot_bgcolor='#283179',paper_bgcolor='#283179',titlefont={
                        'color': 'white',
                        'size': 20},
             xaxis=dict(title='<b></b>',
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

        )}

#####################################3-pre#######################################################################

@app.callback(Output('pre', 'figure'),
              [Input('cc', 'value')])

def update_graph(cc):
        covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == cc][['Country/Region', 'date', 'confirmed']].reset_index()
        covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
        covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()
        days=covid_data_3[covid_data_3['Country/Region'] == cc]['date'].tail(30)

        df = covid_data_3.head(len(covid_data_3))

        df_p = df.tail(30)
        df1 = df.tail(483)
        df = df1.head(453)

        adj = list()
        adj1 = list()
        df_d1 = df_p.loc[:, "date"]
        df_d2 = df_p.loc[:, "daily confirmed"]
        df_d = df.loc[:, "date"]
        df_adj = df.loc[:, "daily confirmed"]
        for ad in df_adj:
            adj.append(float(ad))
        for ad in df_d2:
            adj1.append(float(ad))

        q0 = []
        for d in df_d1:
            o = dt.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
            f = dt.datetime.strftime(o, '%Y-%m-%d')
            q0.append([int(f.split('-')[2])])

        q = []
        for d in df_d:
            o = dt.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
            f = dt.datetime.strftime(o, '%Y-%m-%d')
            q.append([int(f.split('-')[2])])



        prd2=[]
        prd2.append([q0[len(q0)-1][0]+1])
        prd2.append([q0[len(q0) - 1][0] + 2])
        prd2.append([q0[len(q0) - 1][0] + 3])

        rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.85)
        rbf_svr.fit(q, adj)

        tmr=days.tail(1)+datetime.timedelta(days=1)
        tmr=tmr.append(days.tail(1) + datetime.timedelta(days=2))
        tmr = tmr.append(days.tail(1) + datetime.timedelta(days=3))

        return {
            'data': [go.Scatter(
                x=days,
                y=adj1,
                name='<b>reel values</b>',  # Style name/legend entry with html tags
                connectgaps=True  # override default to connect the gaps
            ),go.Scatter(
                x=days,
                y=rbf_svr.predict(q0),
                name='<b>prediction</b>',  # Style name/legend entry with html tags
                connectgaps=True  # override default to connect the gaps
            ),go.Scatter(
                x=tmr,
                y=rbf_svr.predict(prd2),
                name='<b>prediction for the following three days</b>',  # Style name/legend entry with html tags
                line_color='green',
                mode='lines+markers',
                connectgaps=True
            )],
            'layout':
                go.Layout(title='Prediction of daily cases', plot_bgcolor='#283179', paper_bgcolor='#283179', titlefont={
                    'color': 'white',
                    'size': 20},
                          xaxis=dict(title='<b></b>',
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
                          ), legend={
                        'orientation': 'h',
                        'bgcolor': '#283179',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),

                          )}

############################################-main-#####################################################3

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return about
    elif pathname =="/dash":
        return main.dashboard
    elif pathname =="/prediction":
        return predict.predict
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
   app.run_server(debug=True)