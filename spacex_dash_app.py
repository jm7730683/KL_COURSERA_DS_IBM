# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get the launch site options from csv
options_launchSites = []
options_launchSites.append({'label': 'ALL', 'value': 'ALL'})
for launchSite in spacex_df['Launch Site'].unique(): 
    options_launchSites.append({'label': launchSite, 'value': launchSite})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='dropdown_launchSites',
                                    options=options_launchSites,
                                    value='ALL',
                                    placeholder="select a launch site here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='slider_payload',
                                  min=0, max=10000, step=1000,
                                  marks={0: '0 kg',
                                        1000: '1000 kg',
                                        2000: '2000 kg',
                                        3000: '3000 kg',
                                        4000: '4000 kg',
                                        5000: '5000 kg',
                                        6000: '6000 kg',
                                        7000: '7000 kg',
                                        8000: '8000 kg',
                                        9000: '9000 kg',
                                        10000: '10000 kg'},
                                  value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
      Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='dropdown_launchSites', component_property='value')
)
def generate_pie(dropdown_launchSites):
    if (dropdown_launchSites == 'ALL'):
        df  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, values='class', names = 'Launch Site'
                    ,title = 'Launch Successes, all sites')
    else:
        df  = spacex_df[spacex_df['Launch Site'] == dropdown_launchSites]
        df['class_text'] = None
        for ind in df.index:
          if df.at[ind,'class'] == 1:
            df.at[ind,'class_text'] = 'success'
          elif df.at[ind,'class'] == 0:
            df.at[ind,'class_text'] = 'failure'
        
        fig = px.pie(df,  names = 'class_text'
                    ,title = f'Launch Successes and Failures, {dropdown_launchSites}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='dropdown_launchSites',component_property='value'),Input(component_id="slider_payload", component_property="value")]
)
def update_scatter(dropdown_launchSites,slider_payload):
    if dropdown_launchSites == 'ALL':
        low, high = slider_payload
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            spacex_df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        low, high = slider_payload
        df_plot  = spacex_df[spacex_df['Launch Site'] == dropdown_launchSites]
        filter1 = (df_plot['Payload Mass (kg)'] > low) & (df_plot['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df_plot[filter1], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
