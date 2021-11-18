
import pandas as pd
import plotly_express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import functions as fn


# Import data
ger = pd.read_csv("data/germany.csv")

# Medal options
medal_list = "Total Gold Silver Bronze".split()
medal_options = [{'label': medal, 'value': medal} for medal in medal_list]

# slider options: medal-time 
slider_marks = {
    str(year): str(year) for year in range(
        ger["Year"].min(), ger["Year"].max(), 8
    )
}

# Set dataframe medal-time-fig for fig1
df_medal = fn.count_medals(ger, "Year")


# Attribute dropdown options
attr_dict = {
    'Sport':'Sport',  
    'Games':'Year & Season',
    'Season':'Season',  
    'Sex':'Athlete gender', 
    'Age':'Athlete age'
}
attribute_options_dropdown = [
    {'label':name, 'value': attribute} 
    for attribute, name in attr_dict.items()
]


# participants dropdown options
gender_options = [
    {'label':'Both', 'value':'Both'},
    {'label':'Female', 'value':'F'},
    {'label':'Male', 'value':'M'}
]
athlete_dict = { 
    'Age':'Age',
    'Height':'Height',
    'Weight':'Weight'
    
}
unit_dict = {
    'Age':'Age',
    'Height':'Height',
    'Weight':'Weight'
    
}

athlete_options = [
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

    # Main Title
    dbc.Card([
        dbc.CardBody(html.H1(
            'Germany Olympic Sports Statistics', style={'color': 'green'},
            className='text-primary-m-3'
        ))
    ], className='mt-5'),

    # we start with fig1 for medals per year
    dbc.Row([

        # col1 : with medal types and numbers 
        dbc.Col([
            dbc.Card([
                html.H3('Choose medal type:', className='m-3',style={'color': 'blue'}),
                dcc.RadioItems(
                    id='medal-picker-radio', 
                    className='m-1',
                    value="Total",
                    options=medal_options,
                    labelStyle={'display': 'block'}
                )
            ]),
            dbc.Card([
                dbc.Row([
                    html.H3(
                        "Number of medals:", style={'color': 'blue'},
                        className='m-3'
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
        dbc.CardBody(html.H1("Germany's best achievements", style={'color': 'green'},
            className='text-primary-m-4'
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
        # col2 with fig
        dbc.Col([
            dcc.Graph(
                id='top10-graph',
                className=''
            ),
        ])
    ], className='mt-4'),

    #set the third title of histograms
    dbc.Card([
        dbc.CardBody(html.H1("Participants statistics", style={'color': 'green'},
            className='text-primary-m-4'
        ))
    ]),

    # set 2 columns
    dbc.Row([
        dbc.Col([
            dbc.Card([
            # col1 with dropdown data
                html.H3('Choose a gender:', className = 'm-2', style={'color': 'blue'}),
                dcc.RadioItems(
                    id='gender-picker-radio', 
                    className='m-2',
                    value="Both",
                    options=gender_options,
                    labelStyle={'display': 'block'}
                ),

                html.H3('Choose a statistic:', className = 'm-2', style={'color': 'blue'}),
                dcc.RadioItems(
                    id='athlete-radio', 
                    className='m-2',
                    value="Age",
                    options=athlete_options,
                    labelStyle={'display': 'block'}
                ),
            ], className='mt-1'),
        ], lg='8', xl='3'),
        # col2 with fig
        dbc.Col([
            dcc.Graph(
                id='athlete-graph',
                className=''
            ),
        ])
    ], className='mt-4'),
])

@app.callback(
    Output("medals-graph", "figure"),
    Output("total-medals", "children"),
    Output("silver-medals", "children"),
    Output("bronze-medals", "children"),
    Output("gold-medals", "children"),
    Input("medal-picker-radio", "value"),
    Input("time-slider", "value")
)
def update_graph(medal,date):
    """
    Updates graph based on different unputs
    """
    #date represents the list of two points choosen by user and then choose subset of dataframe.
    

    # df of number of medals in Ger per year
    df_medal = fn.count_medals(ger, "Year", "Season")

    # set the period range 
    dff = df_medal[
        (df_medal[df_medal.columns[0]] >= date[0]) & 
        (df_medal[df_medal.columns[0]] <= date[1])]
    
    # get the total medals 
    number_medals = [dff[medal].sum() for medal in medal_list]
    
    # Update figure
    # Color modification based on https://github.com/plotly/plotly.py/issues/2241
    fig = px.bar(
        dff, x="Year", y=medal, color="Season", color_discrete_sequence=["fuchsia", "blue"],
        title=f"Number of {medal} medals between {date[0]} and {date[1]}",
        labels={"value":"Number medals", "variable":"Medal"})

    #set bar width in px.bar based on https://www.codegrepper.com/code-examples/python/Increase+%22bar+width%22+%22px.bar%22
    for data in fig.data: 
        data["width"]= 0.5
   

    return fig, number_medals[0], number_medals[1], number_medals[2], number_medals[3]

# fig of top best statistics of Germany
@app.callback(
    Output("top10-graph", "figure"),
    Input("attribute-dropdown", "value"),
)
def update_graph(chosen_attribute):
    """
    Figure with best achievements for Germany
    """
    # set the df that we want
    df_top = fn.count_medals(ger, chosen_attribute)

    # Sort by attribute and extract top 10
    df_top = df_top.sort_values("Total", ascending=False)
    df_top = df_top.head(10)

    # Update figure
    fig = px.bar(
        df_top, x=chosen_attribute, y=medal_list, color_discrete_sequence=["black", "fuchsia", "light blue", "grey"],
        title=f"Germany's achievements based on {attr_dict[chosen_attribute]}",
        labels={"value":"Number medals", "variable":"Medal"}
    )
    fig.update_layout(barmode='group', xaxis_tickangle=45)

    return fig


@app.callback(
    Output("athlete-graph", "figure"),
    Input("athlete-radio", "value"),
    Input("gender-picker-radio", "value")
)
def update_graph(athlete_attribute, athlete_gender):
    """
    Figure with statistics for athletes
    """
    # get histogram that represents German athletes statistics
    # get fig depending on what we choose
    if athlete_gender == "Both":
        fig = px.histogram(ger, x=athlete_attribute)
    else:
        fig = px.histogram(ger[ger["Sex"]==athlete_gender], x=athlete_attribute)
    
    # that shows axis
    fig.layout.yaxis.title.text = "Number of athletes"
    fig.layout.xaxis.title.text = unit_dict[athlete_attribute]

    return fig


if __name__ == '__main__':
    app.run_server(debug= True)

