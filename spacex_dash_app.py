import pandas as pd
from dash import Dash,dcc,html,Input,Output
import plotly.express as px
df=pd.read_csv('spacex_launch_dash.csv'); sites=sorted(df['Launch Site'].unique()); app=Dash(__name__)
app.layout=html.Div([html.H1('SpaceX Launch Records Dashboard'),dcc.Dropdown(['ALL']+sites,'ALL',id='site'),dcc.RangeSlider(df['Payload Mass (kg)'].min(),df['Payload Mass (kg)'].max(),value=[df['Payload Mass (kg)'].min(),df['Payload Mass (kg)'].max()],id='payload'),dcc.Graph(id='success'),dcc.Graph(id='scatter')])
@app.callback(Output('success','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def update(site,payload):
    d=df[df['Payload Mass (kg)'].between(*payload)]; d=d if site=='ALL' else d[d['Launch Site']==site]
    pie=px.pie(df[df['class']==1],names='Launch Site',title='Successful launches by site') if site=='ALL' else px.pie(d,names='class',title=f'{site} outcomes')
    return pie,px.scatter(d,x='Payload Mass (kg)',y='class',color='Booster Version Category',hover_data=['Launch Site'])
if __name__=='__main__': app.run(debug=True)
