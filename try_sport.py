import pandas as pd
import plotly_express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import functions as fn



# Import data
data_os = pd.read_csv("data/athlete_events.csv")



# Attribute dropdown options
attr_dict = {
    'Sport':'Sport',  
    'Games':'Year & Season',
    'Season':'Season',  
    'Sex':'Athlete gender', 
    'Age':'Athlete age',
    'NOC' : 'NOC'
}
attribute_options_dropdown = [
    {'label':name, 'value': attribute} 
    for attribute, name in attr_dict.items()
]


# participants dropdown options
type_options = [
    {'label':'Fencing', 'value':'Fencing'},
    {'label':'Judo', 'value':'Judo'},
    {'label':'Gymnstics', 'value':'Gymnastics'}
]
sport_dict = { 
    'Age':'Age',
    'NOC':'Country',
    'Sex' : 'Athlete gender',
    'Games':'Games'

}
unit_dict = {
    'Age':'Age',
    'NOC':'Country',
    'Sex':'Athlete gender',
    'Games':'Games'
    
}

sport_options = [
    {'label':name, 'value': attribute} 
    for attribute, name in sport_dict.items()
]


# Set theme settings
stylesheets = [dbc.themes.MATERIA]

# Initiate dashboard

app = dash.Dash(__name__, external_stylesheets=stylesheets,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")]
)

server = app.server  # needed for Heroku to connect to

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody(html.H1("Sport statistics", style={'color': 'green'},
            className='text-primary-m-4'
        ))
    ], className='mt-5'),

    # set 2 columns
   
        dbc.Col([
            dbc.Card([
            # col2 with fig
                html.H3('Choose a sport:', className = 'm-2', style={'color': 'blue'}),
                dcc.RadioItems(
                    id='type-picker-radio', 
                    className='m-2',
                    value="Fencing",
                    options=type_options,
                    labelStyle={'display': 'block'}
                ),

                html.H3('Choose a statistic:', className = 'm-2', style={'color': 'blue'}),
                dcc.RadioItems(
                    id='sport-radio', 
                    className='m-2',
                    value="Age",
                    options=sport_options,
                    labelStyle={'display': 'block'}
                ),
            ], className='mt-1'),
        ], lg='8', xl='2'),
        # 2nd with figure
        dbc.Col([
            dcc.Graph(
                id='sport-graph',
                className=''
            ),
        ])
    ], className='mt-1')
    
@app.callback(
    Output("sport-graph", "figure"),
    Input("sport-radio", "value"),
    Input("type-picker-radio", "value")
)


def update_graph(sport_attribute, sport_type):
    """
    Figure with statistics for athletes

    """
    # get histogram that represents German athletes statistics
    # get fig depending on what we choose
    if sport_type == "Fencing":
        fig = px.histogram(data_os, x=sport_attribute)
    else:
        fig = px.histogram(data_os[data_os["Sport"]==sport_type], x=sport_attribute)
    
    # that shows axis
    fig.layout.yaxis.title.text = "Number of athletes"
    fig.layout.xaxis.title.text = unit_dict[sport_attribute]
   

    return fig

if __name__ == '__main__':
    app.run_server(debug= True)