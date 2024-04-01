# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:48:12 2022

@author: SUHASMR
"""

import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc    
token="pk.eyJ1Ijoibml2ZWRpdGFrIiwiYSI6ImNrZnY2ZzQ1ejBxOGYyeG84eW1rbGoyc3MifQ.8naz8_PAIfrO2-zjT-tObw"
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

dff=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='lat_long')
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
px.set_mapbox_access_token("pk.eyJ1Ijoibml2ZWRpdGFrIiwiYSI6ImNrZnY2ZzQ1ejBxOGYyeG84eW1rbGoyc3MifQ.8naz8_PAIfrO2-zjT-tObw")
# need to pip install statsmodels for strendline='ols' in scatter plot


app = dash.Dash( __name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])
server=app.server
# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='lat_long')
df1=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='payment')
df2=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='transaction')
df3=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='county')
df4=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='trans_bin')
df5=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='hourly(wkwd)')
df6=pd.read_excel("payment_trans_cnty.xlsx",sheet_name='zip_point')

all_options = {
    'DNT': ['MLP1(DNT)', 'MLP2(DNT)', 'MLP3(DNT)','MLP4(DNT)'],
    'PGBT': ['MLP6(PGBT)', 'MLP7(PGBT)', 'MLP8(PGBT)','MLP9(PGBT)','MLP10(PGBT)','MLG5(PGBT)','MLG11(PGBT)',"MLG12(PGBT)"],
    'SRT':['MLG1(SRT)',"MLG2(SRT)","MLG3(SRT)"],
    'CTP':['MLG1(CTP)',"MLG2(CTP)","MLG3(CTP)"],
    '360':['MLG14(360)','MLG15(360)']
}

# fig_ch = px.choropleth_mapbox(df3, geojson=counties, locations='fips', color='No. of Users(Bins)',color_discrete_sequence= px.colors.sequential.YlGn,range_color=[1,20000],
#                 category_orders={'No. of Users(Bins)':["1-100","101-500","501-2000","2001-5000","5001-20000",">20000"]},hover_data=["County","No. of Users"],center={"lat": 33, "lon": -96.88},zoom=6,
#                 template="plotly_dark",title="Users by County(Texas)",opacity=0.5
#                       )
# fig_ch.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig_ch.update_layout(margin={"r":0,"t":50,"l":0,"b":0},width=700,height=500,autosize=True)
# fig_ch.update_layout(legend=dict(orientation="v",yanchor="bottom",y=0.0,xanchor="right",x=1),mapbox_style="mapbox://styles/mapbox/navigation-day-v1") 
# fig_ch.update_geos(fitbounds="locations")
# fig_ch.add_scattermapbox(lat=df['lat'],
#         lon=df['long'],
#         mode='markers+text',
#         marker=go.scattermapbox.Marker(
#             size=15,symbol='bridge',allowoverlap=True
#         ),
#         text=df['Plaza'],textposition = "top right",textfont=dict(size=12, color='black'),customdata=df[["facility_full",'Plaza_full']],hovertemplate='Lat:%{lat}<br>Lon:%{lon}<br>Plaza:%{text}<br>facility:%{customdata[0]}<br>Plaza Name:%{customdata[1]}')
# fig_ch.update_layout(mapbox=dict(
#     accesstoken=token,
#     bearing=0,
#     pitch=0,
#     zoom=15,
   
# ))


fig_ch=go.Figure(go.Scattermapbox(lat=df['lat'],
        lon=df['long'],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=25,color='#d62728',allowoverlap=True
        ),
        text=df['Plaza'],textposition = "top right",textfont=dict(size=12, color='black'),customdata=df[["facility_full",'Plaza_full']],hovertemplate='Lat:%{lat}<br>Lon:%{lon}<br>Plaza:%{text}<br>facility:%{customdata[0]}<br>Plaza Name:%{customdata[1]}'))
fig_ch.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=token,
            bearing=0,
            pitch=0,
            zoom=15,
            style="mapbox://styles/mapbox/streets-v11"
))
    

fig_ch.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_ch.update_layout(margin={"r":0,"t":50,"l":0,"b":0},width=750,height=750,autosize=True)
fig_ch.update_layout(legend=dict(orientation="v",yanchor="bottom",y=0.0,xanchor="right",x=1),template="plotly_dark",title_text="Plazas") 
fig_ch.update_geos(fitbounds="locations")

tabs_styles = {'height': '44px'}

tab_style = {'borderBottom': '1px solid #d6d6d6','padding': '6px','fontWeight': 'bold','color':'black'}

tab_selected_style = {'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#119DFF',
    'color': 'black','padding': '6px'}
   

dropdown_select_graphs=dcc.Dropdown(id='dropdown_grphs',options=[
          {'label':"Payment type",  'value': 'Payment type'},
           {'label': "Transactions", 'value': 'Transactions'},
           {'label': "Transactions(Bins)", 'value': 'Transactions(Bins)'}],placeholder="Select Graph",clearable=False,
           style={'width': '90%', 'margin-left': 15, 'margin-top': 1, 'display':True,"font-weight":'bold','Display':"inline-block","color":"#00ab41"},value="Payment type")

cov_label=html.Label("Covid Timeline:", style={'fontSize':15, 'textAlign':'left'}),
cov_radio=dcc.RadioItems(["precovid","postcovid"],value='precovid',id='cov',inline=True,inputStyle={"margin-left": "20px"})


app.layout = html.Div([dbc.Row([
    dbc.Col([html.H1(id='banner-text-1',
            children='NTTA',style={'color':"green",'backgroundColor': '#119DFF','height':5})],width=7),
    dbc.Col(html.Img(id='banner-logo-1',
        src = app.get_asset_url('NTTA_logo.jfif'),height=50,width=140,style={'margin-left':280,'backgroundColor': '#119DFF'})),
    dbc.Col(html.Img(id='banner-logo-2',
        src = app.get_asset_url('CDMSmith_logo_print_RGB_BlueGr.jpg'),height=50,width=140,style={'margin-left':3,'backgroundColor': '#119DFF'}))
    
    
    ],style={'backgroundColor': '#119DFF'}),
    dcc.Tabs(id="all-tabs-inline", value='tab-1',parent_className='custom-tabs',
    className='custom-tabs-container',
        children=[
        dcc.Tab(label='Transactions', value='tab-1',className='custom-tab',
            selected_className='custom-tab--selected',style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Payment_type', value='tab-2',className='custom-tab',
            selected_className='custom-tab--selected',style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
    html.Label("Facility:", style={'fontSize':15, 'textAlign':'left'}),
    dcc.RadioItems(
        list(all_options.keys()),
        'DNT',
        id='fac',inline=True,inputStyle={"margin-left": "20px"}
    ),


    html.Label("Plazas:", style={'fontSize':15, 'textAlign':'left'}),
    dcc.RadioItems(id='plaza',inline=True,inputStyle={"margin-left": "20px"}),
    html.Div(id="output-div", children=[])

])


# Populate the options of counties dropdown based on states dropdown
@app.callback(
    Output('plaza', 'options'),
    Input('fac', 'value')
)
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


# populate initial values of counties dropdown
@app.callback(
    Output('plaza', 'value'),
    Input('plaza', 'options')
)
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-map', 'figure'),
    #Output('display-map2', 'figure'),
   # Output('display-map3', 'figure'),
    #Input(component_id="dropdown_grphs", component_property="value"),
    Input('plaza', 'value'),
    Input('fac', 'value')
)
def update_grpah(selected_plaza, selected_fac):

    dff = df[(df["facility"]==selected_fac) & (df["Plaza"]==selected_plaza)]
    dff=dff.reset_index(drop=True)
    dff1 =df1[(df1["facility"]==selected_fac) & (df1["Plaza"]==selected_plaza)]
    dff1=dff1.reset_index(drop=True)
    dff2 =df2[(df2["facility"]==selected_fac) & (df2["Plaza"]==selected_plaza)]
    dff2=dff2.reset_index(drop=True)
    dff3 =df4[(df4["facility"]==selected_fac) & (df4["Plaza"]==selected_plaza)]
    dff3=dff3.reset_index(drop=True)

    
    fig_ch.update_layout(mapbox=dict(center=go.layout.mapbox.Center(
        lat=dff['lat'].max(),
        lon=dff['long'].max()
    )))
    
    
    # fig1=px.bar(dff1,x='TripIdentMethod',y='TPTripID',color='cov',barmode='group',title="Payment Type in {1}({0})".format(selected_plaza,selected_fac),text_auto=True)
    # fig1.update_yaxes(matches=None,title_text="No. of Transactions")
    # fig1.update_xaxes(matches=None,type="category",title_text="Payment Type") 
    # fig1.update_layout(height=300,width=600,template='plotly_dark')
    # fig1.update_layout(legend_title_text='Covid Timeline')
    # fig1.update_layout(legend=dict(orientation="v",yanchor="bottom",y=0.0,xanchor="right",x=1))
    
    # fig2=px.bar(dff2,x='cov',y='No. of Transactions',color='cov',title="Transactions in {1}({0})".format(selected_plaza,selected_fac),text_auto=True)
    # fig2.update_yaxes(matches=None,title_text="No. of Transactions")
    # fig2.update_xaxes(matches=None,type="category",title_text="Transactions") 
    # fig2.update_layout(height=225,width=600,template='plotly_dark')
    # fig2.update_layout(legend_title_text='Covid Timeline')
    
    # fig3=px.bar(dff3,x='bin',y='No. of Vehicles',color='cov',barmode='group',title="Transactions in {1}({0})".format(selected_plaza,selected_fac),text_auto=True)
    # fig3.update_yaxes(matches=None,title_text="No. of Vehicles")
    # fig3.update_xaxes(matches=None,type="category",title_text="Transaction(Bins)",categoryorder='array',categoryarray=["1","2","3","4","5-10","11-20",">20"]) 
    # fig3.update_layout(height=300,width=600,template='plotly_dark')
    # fig3.update_layout(legend_title_text='Covid Timeline')
    
    return fig_ch

@app.callback(
    Output('display-map2', 'figure'),
    Input('plaza', 'value'))
def update_ptype(plaza):
    dff1 = df1[df1["Plaza"]==plaza]
    fig1=px.bar(dff1,x='TripIdentMethod',y='TPTripID',color='cov',barmode='group',title="Payment Type in {0}".format(plaza),text_auto=True)
    # fig1=px.pie(dff1,names='TripIdentMethod',values='TPTripID',facet_col='cov',color='TripIdentMethod',hole=0.5,color_discrete_sequence=px.colors.sequential.Blues_r,
    #             title="Payment Type in {0}".format(country_name))
    # fig1.update_traces(textposition='inside', textinfo='percent+label')
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=dff1[dff1['cov']=='precovid']['TripIdentMethod'], values=dff1[dff1['cov']=='precovid']['TPTripID'], name="Precovid",marker_colors=px.colors.sequential.Blues_r,showlegend=False),
                  1, 1)
    fig.add_trace(go.Pie(labels=dff1[dff1['cov']=='postcovid']['TripIdentMethod'], values=dff1[dff1['cov']=='postcovid']['TPTripID'], name="Postcovid",marker_colors=px.colors.sequential.Reds_r,showlegend=False),
                  1, 2)
    
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_text="Payment Type of Transactions in {0}".format(plaza),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='PreCovid', x=0.16, y=0.5, font_size=18, showarrow=False),
                     dict(text='PostCovid', x=0.84, y=0.5, font_size=18, showarrow=False)],height=600,width=930,template='plotly_dark')
    # fig1=go.Figure(data=[go.Pie(
    # labels=dff1['TripIdentMethod'],
    # values=dff1['TPTripID'],
    # textinfo='label+percent',
    # hole=.5,
    # insidetextorientation='radial')])
    fig1.update_yaxes(matches=None,automargin=True,showline=True,mirror=True)
    fig1.update_xaxes(matches=None,showline=True,mirror=True,type="category",title_text="Payment Type") 
    fig1.update_layout(height=400,width=750,template='plotly_dark')
    fig1.update_layout(legend_title_text='Covid Timeline')
#     fig1.update_layout(legend=dict(
#     yanchor="top",
#     y=2,
#     xanchor="left",
#     x=0.7
# ))
    return fig


@app.callback(
    Output('display-map3', 'figure'),
    Input('display-map', 'clickData'))
def update_trans(clickData):
    if clickData is None:
        country_name='MLP1(DNT)'
    else:
        country_name = clickData['points'][0]['text']
    dff3 = df4[df4["Plaza"]==country_name]
    #dff1 = dff[dff['Indicator Name'] == xaxis_column_name]
    #title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    fig3=px.bar(dff3,x='bin',y='No. of Vehicles',color='cov',barmode='group',title="Transactions/Week in {0}".format(country_name),text_auto=True)
    fig3.update_yaxes(matches=None,title_text="No. of Vehicles",automargin=True,showline=True,mirror=True)
    fig3.update_xaxes(matches=None,showline=True,mirror=True,type="category",title_text="Transaction/Week(Bins)",categoryorder='array',categoryarray=["1","2","3","4","5-10","11-20",">20"]) 
    fig3.update_layout(height=370,width=530,template='plotly_dark')
    fig3.update_layout(legend_title_text='')
    fig3.update_layout(legend=dict(orientation="h",yanchor="top",y=1.2,xanchor="left",x=0.5))
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=dff3[dff3['cov']=='precovid']['bin'], values=dff3[dff3['cov']=='precovid']['No. of Vehicles'], name="Precovid",marker_colors=px.colors.sequential.Blues_r,showlegend=False),
                  1, 1)
    fig.add_trace(go.Pie(labels=dff3[dff3['cov']=='postcovid']['bin'], values=dff3[dff3['cov']=='postcovid']['No. of Vehicles'], name="Postcovid",marker_colors=px.colors.sequential.Reds_r,showlegend=False),
                  1, 2)
    
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    fig.update_layout(
        title_text="Transactions/week in {0}".format(country_name),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='PreCovid', x=0.14, y=0.5, font_size=16, showarrow=False),
                     dict(text='PostCovid', x=0.86, y=0.5, font_size=16, showarrow=False)],height=370,width=800,template='plotly_dark')
    
    
#     fig3.update_layout(legend=dict(
#     yanchor="top",
#     y=2,
#     xanchor="left",
#     x=0.7
# ))
    return fig3

@app.callback(
    Output('display-map_hr', 'figure'),
    Input('display-map', 'clickData'))
def update_hourly(clickData):
    if clickData is None:
        country_name='MLP1(DNT)'
    else:
        country_name = clickData['points'][0]['text']
    dff5 = df5[df5["Plaza"]==country_name]
    
    fig_hr = px.line(dff5,x="Trip_hour",y="Avg Transactions",facet_col="Trip_weekday_status",color="cov",height=370,width=1100,title="Hourly Average Transactions in a weekday/weekend in {0}".format(country_name),template="plotly_dark")
    fig_hr.update_xaxes(matches=None,title_text="Hour of the day",tickmode='linear',tickangle=0)
    fig_hr.update_yaxes(matches=None)
    fig_hr.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_hr.update_layout(legend_title_text='Covid Timeline')
    fig_hr.update_layout(legend_title_text='')
    fig_hr.update_layout(legend=dict(orientation="h",yanchor="top",y=1.2,xanchor="left",x=0.85))
    

    return fig_hr

@app.callback(
    Output('display-map_trans', 'figure'),
    Input('display-map', 'clickData'))
def update_trans_simple(clickData):
    if clickData is None:
        country_name='MLP1(DNT)'
    else:
        country_name = clickData['points'][0]['text']
    dff2 = df2[df2["Plaza"]==country_name]
    
    fig_tr=px.bar(dff2,y='No. of Transactions',x='cov',color='cov',barmode='group',facet_col="Trip_weekday_status",title="Transactions/Week in {0}".format(country_name),text_auto=True)
    fig_tr.update_yaxes(automargin=True,showline=True,mirror=True)
    fig_tr.update_xaxes(matches=None,showline=True,mirror=True,type="category",title_text="Transaction/Week") 
    fig_tr.update_layout(height=370,width=1100,template='plotly_dark')
    fig_tr.update_layout(legend_title_text='')
    fig_tr.update_traces(width=1)
    fig_tr.update_layout(legend=dict(orientation="h",yanchor="top",y=1.2,xanchor="left",x=0.85))
    fig_tr.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    

    return fig_tr

@app.callback(
    Output('display-map_zpt', 'figure'),
    #Output('display-map2', 'figure'),
   # Output('display-map3', 'figure'),
    Input(component_id="cov", component_property="value"),
    Input('plaza', 'value'),
    Input('fac', 'value')
)

def zpt(cov,plaza,fac):
    dff6 = df6[df6["Plaza"]==plaza]
    dff6=dff6[dff6["cov"]==cov]
    
    fig_zpt=px.scatter_mapbox(dff6,lat='lat',lon='long',size='Transactions',color='TripIdentMethod',opacity=0.7,center={"lat": 33, "lon": -96.88},hover_data=['Transactions','ZipCode'],zoom=6)

    fig_zpt.update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox_style="mapbox://styles/mapbox/streets-v11")
    fig_zpt.update_layout(margin={"r":0,"t":50,"l":0,"b":0},width=850,height=650,autosize=True)
    fig_zpt.update_layout(legend=dict(orientation="v",yanchor="bottom",y=0.0,xanchor="right",x=1),template="plotly_dark") 
    fig_zpt.update_geos(fitbounds="locations")
    
    
    return fig_zpt


@app.callback(Output("output-div","children"),
    Input("all-tabs-inline", 'value'))


def fin(tab):
    if tab=='tab-1':

        return html.Div(dbc.Row([
                dbc.Col([dcc.Graph(id='display-map',figure={})]),
                dbc.Col([dbc.Row(dcc.Graph(id='display-map_hr',figure={})),html.Hr(),dbc.Row(dcc.Graph(id='display-map_trans',figure={}))])                                                    
                ], align='center')
              )
    else:
        return html.Div([html.Hr(),dbc.Row([cov_radio]),dbc.Row([dbc.Col([dcc.Graph(id='display-map_zpt',figure={})]),dbc.Col([dcc.Graph(id='display-map2',figure={})])])])
        
if __name__ == '__main__':
    app.run_server(debug=False)
