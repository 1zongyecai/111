import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px
import dash_leaflet as dl

cpu = pd.read_json('cpu.json')
cpu_cleaned = cpu.dropna().copy()
cpu_cleaned.loc[cpu['graphics'].str.contains('Rad', na=False), 'graphics'] = 'AMD'
cpu_cleaned.loc[cpu['graphics'].str.contains('Int', na=False), 'graphics'] = 'Intel'
cpu_cleaned.rename(columns={'graphics': 'manufacturer'}, inplace=True)
if 'smt' in cpu_cleaned.columns:
    cpu_cleaned = cpu_cleaned.drop(columns=['smt'])
cpu_data = cpu_cleaned

cpu_cooler = pd.read_json('cpu-cooler.json')
cpu_cooler = cpu_cooler.dropna().copy()

def format_rpm(x):
    if isinstance(x, list) and len(x) == 2:
        return f"{x[0]}-{x[1]}"
    else:
        return str(x)
cpu_cooler['rpm'] = cpu_cooler['rpm'].apply(format_rpm)

def format_noise_level(x):
    if isinstance(x, list) and len(x) == 2:
        return f"{x[0]}-{x[1]}"
    else:
        return str(x)
cpu_cooler['noise_level'] = cpu_cooler['noise_level'].apply(format_noise_level)
###############################################################################

app = Dash(__name__)

app.layout = html.Div([
  ###################################################################################    
    # html.Div([
    # ###################################################################################
        html.Div([
            html.H3('Pick Your CPU'),
            html.Div([
                dcc.Graph(
                    id='cpu_price_histogram',
                    figure=px.histogram(cpu_data, x="price", nbins=50, title="CPU Price Distribution"),
                    style={'width': '100%', 'height': '350px','backgroundColor': '#87CEEB'}
                    ),
                ], style={'width': '98%','margin': '0.5%'}),
            
            html.Label('Choose Your Price Range'),
            html.Br(),
            #########################################################################
            html.Div([ 
                dcc.RangeSlider(
                    id='price_slider_cpu',
                    min=cpu_data['price'].min(),
                    max=cpu_data['price'].max(),
                    value=[cpu_data['price'].min(), cpu_data['price'].max()],
                    step=1,
                    updatemode='mouseup'
                )
            ], style={'width': '98%', 'margin': 'o auto'}),
            ############################################################################
            html.Div(id='display_choose_your_price_range_cpu', style={'margin-top': '10px'}),
            html.Label('Select Manufacturer'),
            dcc.Checklist(
                id='manufacturer_checklist',
                options=[{'label': manufacturer, 'value': manufacturer} for manufacturer in ['Intel', 'AMD']],
                value=['Intel'],
                inline=False
            ),
            html.Label('Select Core Count'),
            dcc.Checklist(
                id='core_count_checklist',
                options=[{'label': str(core), 'value': core} for core in sorted(cpu_data['core_count'].unique())],
                value=[4], 
                inline=True
            ),
            html.Div(id='output_table_cpu')
        ], style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'top','backgroundColor': '#87CEEB','margin': '0 5%'}),
    ###################################################################################
        # html.Hr(style={'width': '49%'}),

        html.Div(style={'width': '0.5%', 'display': 'inline-block', 'border-right': '2px solid white', 'height': '100vh'}),
        # html.Div(style={'height': '50px'}),
        html.Div([
            html.H3('Pick Your CPU Cooler'),

            html.Div([
                dcc.Graph(
                    id='cooler_price_histogram',
                    figure=px.histogram(cpu_cooler, x="price", nbins=50, title="CPU Cooler Price Distribution"),
                    style={'width': '100%', 'height': '350px','backgroundColor': '#87CEEB'}
                    ),
                ], style={'width': '98%', 'height': '200px','margin': '0 5%'}),

            
            html.Label('Choose Your Price Range'),
            html.Br(),
            ############################################################################
            html.Div([
                dcc.RangeSlider(
                    id='price_slider_cooler',
                    min=cpu_cooler['price'].min(),
                    max=cpu_cooler['price'].max(),
                    value=[cpu_cooler['price'].min(), cpu_cooler['price'].max()],
                    step=0.01,
                    marks={int(price): f"${price}" for price in cpu_cooler['price'].unique()},
                )
            ], style={'width': '100%', 'margin': '0 auto'}),
            ############################################################################
            html.Div(id='display_choose_your_price_range_cooler', style={'margin-top': '10px'}),
            html.Label('Select a Color'),
            dcc.Dropdown(
                id='color_dropdown',
                options=[{'label': color, 'value': color} for color in cpu_cooler['color'].unique()],
                multi=True,
                value=['Black'],
                placeholder="Select a Color"
            ),
            html.Label('Select a Size'),
            dcc.Dropdown(
                id='size_dropdown',
                options=[{'label': size, 'value': size} for size in cpu_cooler['size'].unique()],
                multi=True,
                value=[240],
                placeholder="Select a Size"
            ),
            html.Div(id='output_table_cooler')
        ], style={'width': '32.5%', 'display': 'inline-block', 'vertical-align': 'top','backgroundColor': '#87CEEB','margin': '0 5%'}),
        # ,'margin': '5%','height': '100px'
    ###################################################################################
    # ],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}),
  ###################################################################################
    html.Div(style={'width': '0.5%', 'display': 'inline-block', 'border-right': '2px solid white', 'height': '100vh'}),
    html.Div([
        html.H3("Budget"),
        #price
        # html.Label("Enter CPU Name:"),
        dcc.Input(id='cpu-input', type='text', placeholder='Enter CPU name'),
        html.Br(),
        # html.Label("Enter CPU-cooler Name:"),
        dcc.Input(id='cpu-cooler-input', type='text', placeholder='Enter CPU-cooler name'),
    
        html.Div(id='output-table'),
        html.Hr(style={'width': '100%'}),
        #map
        html.H3("JB Hi-Fi Nearby"),
        dl.Map(
        [
            dl.TileLayer(),
            dl.Marker(position=(-33.884281660673814, 151.1579611119875), children=dl.Tooltip('JB Hi-Fi Leichhardf')),
            dl.Marker(position=(-33.88321284915763, 151.19572661630812), children=dl.Tooltip('JB Hi-Fi Broadway')),
            dl.Marker(position=(-33.87630087811186, 151.20697043691268), children=dl.Tooltip('JB Hi-Fi World Square')),
            dl.Marker(position=(-33.87138377442834, 151.20757125175416), children=dl.Tooltip('JB Hi-Fi Galeries Victoria')),
            dl.Marker(position=(-33.86860441660656, 151.209030373512), children=dl.Tooltip('JB Hi-Fi City - Westfield Sydney')),
            dl.Marker(position=(-33.88849628701466, 151.18712997249523), children=[
                dl.Tooltip('University of Sydney'),
                dl.Popup('University of Sydney')
            ])
        ],
        bounds=[
            [-33.88849628701466, 151.18712997249523],  # Left-bottom
            [-33.88849628701466, 151.18712997249523]   # Right-top
        ],
        zoomControl=False,
        doubleClickZoom=False,
        center=(-33.88849628701466, 151.18712997249523),  # University of Sydney
        zoom=15,  # Initial zoom level
        style={'height': '200px'}
    ),
        html.Hr(style={'width': '100%'}),
        html.H3('Select a Link to Visit'),

        dcc.Link('CPL Online', href='https://www.cplonline.com.au/', target='_blank'),
        html.Br(),  

        dcc.Link('PCPartPicker List', href='https://pcpartpicker.com/list/', target='_blank'),
        html.Br(),  

        dcc.Link('Centre Com', href='https://www.centrecom.com.au/', target='_blank'),
        html.Br(),  

        dcc.Link('Jb-Hifi', href='https://www.jbhifi.com.au//', target='_blank'),
        html.Br(), 

        dcc.Link('Scorptec', href='https://www.scorptec.com.au/', target='_blank')

    ],style={'width': '32.5%', 'display': 'inline-block', 'vertical-align': 'top','backgroundColor': '#87CEEB'})
  ###################################################################################

    # ],style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top', 'backgroundColor': 'white'})
######################################################################
@app.callback(
    [Output('price_slider_cpu', 'marks'),
     Output('display_choose_your_price_range_cpu', 'children')],
    [Input('price_slider_cpu', 'value')]
)

def display_price_range_cpu(price_range_cpu):
    marks = {
        int(price_range_cpu[0]): f'${price_range_cpu[0]:.2f}',
        int(price_range_cpu[1]): f'${price_range_cpu[1]:.2f}'
    }
    return marks, f'Price Range: ${price_range_cpu[0]:.2f} - ${price_range_cpu[1]:.2f}'

@app.callback(
    Output('output_table_cpu', 'children'),
    [Input('price_slider_cpu', 'value'),
     Input('manufacturer_checklist', 'value'),
     Input('core_count_checklist', 'value')]
)
def update_table_cpu(price_range_cpu, selected_manufacturers, selected_core):
    filtered_df = cpu_data[
        (cpu_data['price'] >= price_range_cpu[0]) & 
        (cpu_data['price'] <= price_range_cpu[1]) & 
        (cpu_data['manufacturer'].isin(selected_manufacturers)) & 
        (cpu_data['core_count'].isin(selected_core))
    ]
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        page_size=4,
        style_table={'overflowY': 'auto'}
)
],style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top', 'backgroundColor': '#87CEEB'})


@app.callback(
    [Output('price_slider_cooler', 'marks'),
     Output('display_choose_your_price_range_cooler', 'children')],
    [Input('price_slider_cooler', 'value')]
)
def display_price_range_cooler(price_range_cooler):
    marks = {
        int(price_range_cooler[0]): f'${price_range_cooler[0]:.2f}',
        int(price_range_cooler[1]): f'${price_range_cooler[1]:.2f}'
    }
    return marks, f'Price Range: ${price_range_cooler[0]:.2f} - ${price_range_cooler[1]:.2f}'

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in filtered_cpu_cooler.columns],
        data=filtered_cpu_cooler.to_dict('records'),
        page_size=4,
        style_table={'overflowY': 'auto'}
)


@app.callback(
    Output('output_table_cooler', 'children'),
    [Input('price_slider_cooler', 'value'),
     Input('color_dropdown', 'value'),
     Input('size_dropdown', 'value')]
)
def update_table_cooler(price_range_cooler, color_list, size_list):
    color_list = color_list or []
    size_list = size_list or []
    filtered_cpu_cooler = cpu_cooler[
        (cpu_cooler['price'].between(price_range_cooler[0], price_range_cooler[1])) & 
        (cpu_cooler['color'].isin(color_list)) &
        (cpu_cooler['size'].isin(size_list))
    ]

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in filtered_cpu_cooler.columns],
        data=filtered_cpu_cooler.to_dict('records'),
        page_size=4,  
        style_table={'overflowY': 'auto'}  
    )

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in filtered_cpu_cooler.columns],
        data=filtered_cpu_cooler.to_dict('records')
    )
@app.callback(
    Output('output-table', 'children'),
    [Input('cpu-input', 'value'),
     Input('cpu-cooler-input', 'value')]
)
def update_table(cpu_name, cpu_cooler_name):
    
    cpu_price = cpu[cpu['name'] == cpu_name]['price'].values
    cpu_price = cpu_price[0] if len(cpu_price) > 0 else 0
    
    
    cpu_cooler_price = cpu_cooler[cpu_cooler['name'] == cpu_cooler_name]['price'].values
    cpu_cooler_price = cpu_cooler_price[0] if len(cpu_cooler_price) > 0 else 0
    
    total_price = cpu_price + cpu_cooler_price
    
    
    data = [
        {'Item': 'CPU', 'Name': cpu_name if cpu_name else '-', 'Price': cpu_price},
        {'Item': 'CPU-cooler', 'Name': cpu_cooler_name if cpu_cooler_name else '-', 'Price': cpu_cooler_price},
        {'Item': 'Total', 'Name': '-', 'Price': total_price}
    ]
    
  
    table = dash_table.DataTable(
        columns=[
            {'name': 'Item', 'id': 'Item'},
            {'name': 'Name', 'id': 'Name'},
            {'name': 'Price', 'id': 'Price'}
        ],
        data=data,
        style_table={'width': '50%', 'margin': 'auto'},
        style_cell={'text-align': 'center'},
        style_header={'background-color': '#f2f2f2', 'font-weight': 'bold'}
    )
    
    return table

if __name__ == '__main__':
    app.run_server(debug=True)
