#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash.dependencies as dd
from dash.exceptions import PreventUpdate
import base64
from dash import Input, Output

# Creating the dataset manually
world_cup_data = [
    {"Year": 1930, "Winner": "Uruguay", "Runner-up": "Argentina"},
    {"Year": 1934, "Winner": "Italy", "Runner-up": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy", "Runner-up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-up": "Brazil"},
    {"Year": 1954, "Winner": "Germany", "Runner-up": "Hungary"},
    {"Year": 1958, "Winner": "Brazil", "Runner-up": "Sweden"},
    {"Year": 1962, "Winner": "Brazil", "Runner-up": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England", "Runner-up": "Germany"},
    {"Year": 1970, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1974, "Winner": "Germany", "Runner-up": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina", "Runner-up": "Netherlands"},
    {"Year": 1982, "Winner": "Italy", "Runner-up": "Germany"},
    {"Year": 1986, "Winner": "Argentina", "Runner-up": "Germany"},
    {"Year": 1990, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 1994, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1998, "Winner": "France", "Runner-up": "Brazil"},
    {"Year": 2002, "Winner": "Brazil", "Runner-up": "Germany"},
    {"Year": 2006, "Winner": "Italy", "Runner-up": "France"},
    {"Year": 2010, "Winner": "Spain", "Runner-up": "Netherlands"},
    {"Year": 2014, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 2018, "Winner": "France", "Runner-up": "Croatia"},
    {"Year": 2022, "Winner": "Argentina", "Runner-up": "France"},
]

# Convert to DataFrame
df = pd.DataFrame(world_cup_data)

# Count the number of wins per country
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Dash app setup
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Winners Dashboard"),
    
    # Country Dropdown
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All Countries', 'value': 'All'}] +
                [{'label': country, 'value': country} for country in win_counts['Country']],
        value='All',
        placeholder='Select a country'
    ),
    
    # Year Dropdown
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': 'All Years', 'value': 'All'}] +
                [{'label': str(year), 'value': year} for year in df['Year']],
        value='All',
        placeholder='Select a year'
    ),
    
    # Output for country win count
    html.Div(id='country-output', style={'font-size': '20px', 'margin-top': '20px'}),
    
    # Output for winner/runner-up information
    html.Div(id='year-output', style={'font-size': '20px', 'margin-top': '20px'}),
    
    # Choropleth Map
    dcc.Graph(id='choropleth-map')
])

# Callback to update the choropleth map based on selected country
@app.callback(
    dd.Output('choropleth-map', 'figure'),
    [dd.Input('country-dropdown', 'value')]
)
def update_map(selected_country):
    display_data = win_counts.copy()
    
    if selected_country != 'All':
        display_data['Wins'] = display_data.apply(
            lambda row: row['Wins'] if row['Country'] == selected_country else 0.5, axis=1
        )
    
    fig = px.choropleth(
        display_data,
        locations='Country',
        locationmode='country names',
        color='Wins',
        title='FIFA World Cup Wins by Country',
        color_continuous_scale='Blues',
        range_color=[0, display_data['Wins'].max()]
    )
    return fig

# Callback to update the winner and runner-up information based on selected year
@app.callback(
    dd.Output('year-output', 'children'),
    [dd.Input('year-dropdown', 'value')]
)
def update_year_output(selected_year):
    if selected_year and selected_year != 'All':
        match = df[df['Year'] == selected_year]
        if not match.empty:
            match = match.iloc[0]
            return f"In {selected_year}, the winner was {match['Winner']} and the runner-up was {match['Runner-up']}"
        else:
            return "No data available for the selected year."
    return "Select a year to see the winner and runner-up."

# Callback to update the country win count
@app.callback(
    dd.Output('country-output', 'children'),
    [dd.Input('country-dropdown', 'value')]
)
def update_country_output(selected_country):
    if selected_country and selected_country != 'All':
        wins = win_counts[win_counts['Country'] == selected_country]['Wins'].values
        if len(wins) > 0:
            return f"{selected_country} has won the World Cup {wins[0]} times."
        else:
            return f"{selected_country} has never won the World Cup."
    return ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




