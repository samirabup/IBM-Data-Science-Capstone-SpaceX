
# ============================================================
# 1. Import Required Libraries
# ============================================================

import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# ============================================================
# 2. Read SpaceX Launch Data
# ============================================================

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# ============================================================
# 3. Create Dash Application
# ============================================================

app = dash.Dash(__name__)


# ============================================================
# 4. Create Application Layout
# ============================================================

app.layout = html.Div(children=[

    # Dashboard Title
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 40
        }
    ),

    html.Br(),

    # Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Launch Success Pie Chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    # TASK 3: Payload Range Label
    html.P("Payload range (Kg):"),

    # Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            1000: '1000',
            2000: '2000',
            3000: '3000',
            4000: '4000',
            5000: '5000',
            6000: '6000',
            7000: '7000',
            8000: '8000',
            9000: '9000',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Payload vs Launch Success Scatter Chart
    dcc.Graph(id='success-payload-scatter-chart')

])


# ============================================================
# 5. TASK 2: Pie Chart Callback
# ============================================================

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):

    # Filter all launch sites or selected site
    if entered_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

    # Count successful and unsuccessful launches
    success_counts = (
        filtered_df['class']
        .value_counts()
        .rename_axis('class')
        .reset_index(name='count')
    )

    # Create pie chart
    fig = px.pie(
        success_counts,
        names='class',
        values='count',
        title='Launch Success Counts'
    )

    return fig


# ============================================================
# 6. TASK 4: Scatter Chart Callback
# ============================================================

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)

def get_scatter_chart(entered_site, payload_range):

    # Get selected payload range
    low, high = payload_range

    # Filter data based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # Show all launch sites
    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Launch Success for All Sites'
        )

    # Show selected launch site
    else:

        site_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation Between Payload and Launch Success for {entered_site}'
        )

    return fig


# ============================================================
# 7. Run the Dash Application
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
