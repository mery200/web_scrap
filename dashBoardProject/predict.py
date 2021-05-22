
import dash_core_components as dcc
import dash_html_components as html

#################################################################################

import pandas as pd
new_dogs = pd.read_csv("C:\\Users\\boukh\\OneDrive\\Bureau\\pfa\\dashBoardProject\\3c7f0f4f-82f9-4ade-9c6b-fe5f1bfc2273_Data.csv")
z=new_dogs["Country Name"].unique()



predict = html.Div([
html.Div([

                    html.P('Select Country:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='cc',
                                  multi=False,
                                  clearable=True,
                                  value='Morocco',
                                  placeholder='Select Countries',
                                  options=[{'label': c, 'value': c}
                                           for c in (z[:217])
                                           ], className='dcc_compon'),
                    dcc.Graph(id="pre"),

        ], className="create_container", id="cross-filter-options"),
html.Div([
            html.Div([
                      dcc.Graph(id='id1',
                              config={'displayModeBar': 'hover'}),
                              ], className="create_container six columns"),

            html.Div([
                    dcc.Graph(id="id2")
                                ], className="create_container five columns"),
            html.Div([
                    dcc.Graph(id="id3")
                         ], className="create_container six columns"),
            html.Div([
                    dcc.Graph(id="id4")
                                ], className="create_container five columns"),
            html.Div([
                    dcc.Graph(id="id5")
                         ], className="create_container six columns"),
            html.Div([
                    dcc.Graph(id="id6")
                                ], className="create_container five columns"),
], className="row"),



])


