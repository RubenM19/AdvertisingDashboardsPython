import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Cargar y preparar los datos
df = pd.read_csv('Advertising.csv', index_col=0)

# Definir colores personalizados
colors = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'accent': '#2ecc71'
}

# Diseño de la aplicación
app.layout = html.Div([
    # Encabezado
    html.Div([
        html.H1('Análisis de Impacto Publicitario en Ventas',
                style={'textAlign': 'center', 'color': colors['text'], 
                       'fontFamily': 'Helvetica', 'marginBottom': '30px',
                       'marginTop': '20px', 'fontSize': '36px'}),
        html.P('Análisis interactivo de la relación entre inversión publicitaria y ventas por canal',
               style={'textAlign': 'center', 'color': colors['text'], 
                      'fontSize': '18px', 'marginBottom': '40px'})
    ], style={'backgroundColor': colors['background'], 'padding': '20px'}),
    
    # Contenedor principal
    html.Div([
        # Panel izquierdo - Controles
        html.Div([
            html.H3('Controles de Visualización',
                    style={'color': colors['text'], 'marginBottom': '20px'}),
            
            html.Label('Seleccione Canal Publicitario:',
                      style={'fontSize': '16px', 'color': colors['text']}),
            dcc.Dropdown(
                id='channel-selector',
                options=[
                    {'label': 'TV', 'value': 'TV'},
                    {'label': 'Radio', 'value': 'Radio'},
                    {'label': 'Periódico', 'value': 'Newspaper'}
                ],
                value='TV',
                style={'marginBottom': '20px'}
            ),
            
            html.Div([
                html.H4('Estadísticas Generales',
                        style={'color': colors['text'], 'marginTop': '30px'}),
                html.Div(id='stats-container')
            ])
        ], style={'width': '25%', 'padding': '20px', 'backgroundColor': 'white',
                  'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)',
                  'borderRadius': '10px'}),
        
        # Panel derecho - Gráficos
        html.Div([
            # Gráfico de dispersión principal
            dcc.Graph(id='scatter-plot',
                     style={'height': '500px', 'marginBottom': '20px'}),
            
            # Gráficos adicionales
            html.Div([
                dcc.Graph(id='distribution-plot',
                         style={'height': '300px'})
            ])
        ], style={'width': '73%', 'marginLeft': '2%'})
    ], style={'display': 'flex', 'margin': '20px'}),
], style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# Callbacks
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('distribution-plot', 'figure'),
     Output('stats-container', 'children')],
    [Input('channel-selector', 'value')]
)
def update_graphs(selected_channel):
    # Gráfico de dispersión
    scatter_fig = px.scatter(df, x=selected_channel, y='Sales',
                            trendline="ols",
                            trendline_color_override=colors['secondary'])
    
    scatter_fig.update_traces(
        marker=dict(size=10, color=colors['primary'], opacity=0.7),
        selector=dict(mode='markers')
    )
    
    scatter_fig.update_layout(
        title=f'Relación entre Inversión en {selected_channel} y Ventas',
        template='plotly_white',
        hovermode='closest',
        xaxis_title=f'Inversión en {selected_channel} (miles de $)',
        yaxis_title='Ventas (miles de $)',
        showlegend=False
    )
    
    # Gráfico de distribución
    dist_fig = make_subplots(rows=1, cols=2,
                            subplot_titles=(f'Distribución de Inversión en {selected_channel}',
                                          'Distribución de Ventas'))
    
    dist_fig.add_trace(
        go.Histogram(x=df[selected_channel], nbinsx=30,
                     marker_color=colors['primary'],
                     opacity=0.7),
        row=1, col=1
    )
    
    dist_fig.add_trace(
        go.Histogram(x=df['Sales'], nbinsx=30,
                     marker_color=colors['secondary'],
                     opacity=0.7),
        row=1, col=2
    )
    
    dist_fig.update_layout(
        template='plotly_white',
        showlegend=False,
        height=300
    )
    
    # Estadísticas
    correlation = df[selected_channel].corr(df['Sales']).round(3)
    stats = html.Div([
        html.P([
            html.Strong('Correlación con Ventas: '),
            f'{correlation}'
        ], style={'fontSize': '14px', 'marginBottom': '10px'}),
        html.P([
            html.Strong('Inversión Promedio: '),
            f'${df[selected_channel].mean():,.2f}K'
        ], style={'fontSize': '14px', 'marginBottom': '10px'}),
        html.P([
            html.Strong('Inversión Máxima: '),
            f'${df[selected_channel].max():,.2f}K'
        ], style={'fontSize': '14px', 'marginBottom': '10px'}),
        html.P([
            html.Strong('Ventas Promedio: '),
            f'${df["Sales"].mean():,.2f}K'
        ], style={'fontSize': '14px'})
    ])
    
    return scatter_fig, dist_fig, stats

if __name__ == '__main__':
    app.run_server(debug=True)