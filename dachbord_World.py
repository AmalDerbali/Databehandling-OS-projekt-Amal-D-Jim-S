import pandas as pd
import plotly_express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import functions as fn


# Import data
data_os = pd.read_csv("data/athlete_events.csv")


# Medal options
medal_list = "Total Gold Silver Bronze".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]

# slider options: medal-time
slider_marks = {
    str(year): str(year) for year in range(
        data_os["Year"].min(), data_os["Year"].max(), 10
    )
}

# Set dataframe medal-time-fig for fig1
df_medal = fn.count_medals(data_os, "Year")


# Attribute dropdown options
attr_dict = {
    'Sport':'Sports',  
    'Games':'Year & Season',
    'Season':'Season',  
    'Sex':'Athlete gender', 
    'Age':'Athlete age'
}
attribute_options_dropdown = [
    {'label':name, 'value': attribute} 
    for attribute, name in attr_dict.items()
]


# sports dropdown options
type_options = [
    {'label':'Fencing', 'value':'Fencing'},
    {'label':'Judo', 'value':'Judo'},
    {'label':'Gymnstics', 'value':'Gymnastics'}
]
athlete_dict = { 
    'Age':'Age',
    'NOC':'Country',
    'Sex' : 'Athlete gender'
    
}
unit_dict = {
    'Age':'Age',
    'NOC':'Country',
    'Sex' : 'Athlete gender'
    
}

sport_options = [
    {'label':name, 'value': attribute} 
    for attribute, name in athlete_dict.items()
]


# Set theme settings
stylesheets = [dbc.themes.MATERIA]

# Initiate dashboard

app = dash.Dash(__name__, external_stylesheets=stylesheets,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")]
)

server = app.server  # needed for Heroku to connect to

app.layout = dbc.Container([

    # set Title
    dbc.Card([
        dbc.CardBody(html.H1(
            'World Olympic Sports Statistics', style={'color': 'green'},
            className='text-primary-m-3'
        ))
    ], className='mt-3'),

    # we start with fig1 for medals per year
    dbc.Row([

        # col1 : with medal types and numbers 
        dbc.Col([
            dbc.Card([
                html.H3('Choose medal type:', className='m-2', style={'color': 'blue'}),
                dcc.RadioItems(
                    id='medal-picker-radio', 
                    className='m-2',
                    value="Total",
                    options=medal_options,
                    labelStyle={'display': 'block'}
                )
            ]),
            dbc.Card([
                dbc.Row([
                    html.H3(
                        "Number of medals:", style={'color': 'blue'},
                        className='m-2'
                    ),
                    dbc.Col([
                        html.P("Total:", className='m-2'),
                        html.P("Gold:", className='m-2'),
                        html.P("Silver:", className='m-2'),
                        html.P("Bronze:", className='m-2'),
                    ]),
                    dbc.Col([
                        html.P(id='total-medals', className='m-2'),
                        html.P(id='gold-medals', className='m-2'),
                        html.P(id='silver-medals', className='m-2'),
                        html.P(id='bronze-medals', className='m-2'),
                    ])
                ])
            ], className='mt-1')
        ], lg='8', xl='2'),

        #col2: with figure
        dbc.Col([
            dcc.Graph(
                id='medals-graph', 
                className=''
            ),
            dcc.RangeSlider(
                id='time-slider', 
                className='',
                min = df_medal[df_medal.columns[0]].min(), 
                max = df_medal[df_medal.columns[0]].max(), 
                step = 2,
                dots=True, 
                value=[
                    df_medal[df_medal.columns[0]].min(), 
                    df_medal[df_medal.columns[0]].max()
                ],
                marks = slider_marks
            ),
        ]),
    ], className='mt-4'),

    #set the second title, for the second fig
    dbc.Card([
        dbc.CardBody(html.H1("World top sports in the Olympic games",
            className='text-primary-m-4', style={'color': 'green'}
        ))
    ], className='mt-5'), 
    
    # set 2 columns
    dbc.Row([
        # col1 with dropdown data
        dbc.Col([
            html.H3('Choose a statistic:', className = 'm-2', style={'color': 'blue'}),
            dcc.Dropdown(
                id = 'attribute-dropdown',
                className = 'm-2',
                value = "Sport",
                options = attribute_options_dropdown
            ),
        ], lg='8', xl='2'),
        #col2 with fig
        dbc.Col([
            dcc.Graph(
                id='top10-graph',
                className=''
            ),
        ])
    ], className='mt-4'),

    #set the third title of histograms
    dbc.Card([
        dbc.CardBody(html.H1("Sport statistics", style={'color': 'green'},
            className='text-primary-m-4'
        ))
    ]),

    # set 2 columns
    dbc.Row([
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
    ], className='mt-4'),
    

    html.Footer([
        html.H3("Olympic Sports Statistics", className="h5")],
        className="navbar fixed-bottom"),
    

], fluid=True)
  

@app.callback(
    Output("medals-graph", "figure"),
    Output("total-medals", "children"),
    Output("silver-medals", "children"),
    Output("bronze-medals", "children"),
    Output("gold-medals", "children"),
    Input("medal-picker-radio", "value"),
    Input("time-slider", "value")
)
def update_graph(medal,time_index):
    """
    Updates graph based on different unputs
    """
    # date represents the list of two points choosen by user and then choose subset of dataframe.
    
    # df of number of medals per year
    # Save number of medals per year
    df_medal = fn.count_medals(data_os, "Year", "Season")

    # set the period range 
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= time_index[0]) & 
        (df_medal[df_medal.columns[0]] <= time_index[1])
    ]
    
    # get the total medals 
    number_medals = [dff[medal].sum() for medal in medal_list]
    
    # Update figure
    fig = px.bar(
        dff, x="Year", y=medal, color="Season",
        title=f"The number of {medal} medals between {time_index[0]} and {time_index[1]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )

    #set bar width in px.bar based on https://www.codegrepper.com/code-examples/python/Increase+%22bar+width%22+%22px.bar%22
    for data in fig.data:
        data["width"]= 0.5
    
    return fig, number_medals[0], number_medals[1], number_medals[2], number_medals[3]

# fig of wolrd top best statistics
@app.callback(
    Output("top10-graph", "figure"),
    Input("attribute-dropdown", "value"),
)
def update_graph(chosen_attribute):
    """
    Figure with best achievements for Germany

    """
    # set the df that we want
    df_top = fn.count_medals(data_os, chosen_attribute)

    # get top 10 df and by attribute
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(10)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list,
        title=f"World best statistics based on {attr_dict[chosen_attribute]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group', xaxis_tickangle=45)

    return fig


@app.callback(
    Output("sport-graph", "figure"),
    Input("sport-radio", "value"),
    Input("type-picker-radio", "value")
)

def update_graph(sport_attribute, sport_type):
    """
    Figure with statistics for types of sports

    """
    # get histogram that represents sport statistics
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