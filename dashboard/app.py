"""
Interactive Dashboard for New Jersey Consolidation Analysis

A comprehensive Dash application that provides an interactive interface
for exploring the potential benefits of municipal consolidation in Northern New Jersey.
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_collection import NJDataCollector
from analysis import NJConsolidationAnalyzer
from visualizations import NJVisualizationCreator

class NJConsolidationDashboard:
    """Interactive dashboard for New Jersey consolidation analysis"""
    
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Set up the dashboard layout"""
        
        # Header
        header = dbc.NavbarSimple(
            brand="New Jersey Consolidation Analysis",
            brand_href="#",
            color="primary",
            dark=True,
            className="mb-4"
        )
        
        # Introduction card
        intro_card = dbc.Card([
            dbc.CardBody([
                html.H4("The Case for Greater Jersey City", className="card-title"),
                html.P([
                    "This dashboard explores the potential for consolidating Northern New Jersey's ",
                    "fragmented municipalities into a single, more efficient city. Based on the concept ",
                    "presented in ",
                    html.A("this article", href="https://papaghanoush.substack.com/p/new-jerseys-potential-and-a-plea", 
                          target="_blank"),
                    ", a consolidated Northern New Jersey would become the ",
                    html.Strong("3rd largest city in the United States"),
                    " with over 3.6 million people."
                ]),
                dbc.Alert([
                    html.H5("Key Insight", className="alert-heading"),
                    "If Bergen, Essex, Hudson, Passaic, and Union counties were consolidated into one city, "
                    "it would rank 58th globally, ahead of Madrid, Buenos Aires, and Toronto."
                ], color="info")
            ])
        ])
        
        # Main content tabs
        tabs = dbc.Tabs([
            dbc.Tab(label="Population Analysis", tab_id="population"),
            dbc.Tab(label="World Rankings", tab_id="rankings"),
            dbc.Tab(label="County Breakdown", tab_id="counties"),
            dbc.Tab(label="Economic Impact", tab_id="economic"),
            dbc.Tab(label="Municipality Sizes", tab_id="sizes")
        ], id="main-tabs", active_tab="population")
        
        # Content area
        content = html.Div(id="tab-content", className="mt-4")
        
        # Footer
        footer = dbc.Card([
            dbc.CardBody([
                html.P([
                    "Data sources: US Census Bureau, New Jersey Department of State, ",
                    "and analysis based on municipal consolidation research."
                ], className="text-muted small"),
                html.P([
                    "Inspired by: ",
                    html.A("New Jersey's Potential and a Plea for a Greater Jersey City", 
                          href="https://papaghanoush.substack.com/p/new-jerseys-potential-and-a-plea",
                          target="_blank")
                ], className="text-muted small")
            ])
        ], className="mt-4")
        
        # Assemble layout
        self.app.layout = dbc.Container([
            header,
            intro_card,
            tabs,
            content,
            footer
        ], fluid=True)
    
    def setup_callbacks(self):
        """Set up dashboard callbacks"""
        
        @self.app.callback(
            Output('tab-content', 'children'),
            Input('main-tabs', 'active_tab')
        )
        def render_tab_content(active_tab):
            if active_tab == "population":
                return self.create_population_tab()
            elif active_tab == "rankings":
                return self.create_rankings_tab()
            elif active_tab == "counties":
                return self.create_counties_tab()
            elif active_tab == "economic":
                return self.create_economic_tab()
            elif active_tab == "sizes":
                return self.create_sizes_tab()
            else:
                return html.Div("Select a tab to view content")
    
    def create_population_tab(self):
        """Create the population analysis tab"""
        
        # Load data
        try:
            municipalities = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
            scenarios = pd.read_csv(self.data_dir / 'consolidation_scenarios.csv')
        except FileNotFoundError:
            return dbc.Alert("Data not found. Please run data collection first.", color="warning")
        
        target_region = municipalities[municipalities['in_target_region']]
        
        # Population comparison chart
        comparison_data = {
            'Scenario': ['Current (Fragmented)', '5-County Consolidation', '3-County Core'],
            'Population': [
                target_region['population_2020'].sum(),
                3610711,
                2500000
            ],
            'Municipalities': [
                len(target_region),
                1,
                1
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Population Comparison', 'Municipalities Count'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['Population'],
                name='Population',
                marker_color=['#1f77b4', '#2ca02c', '#ff7f0e'],
                text=[f"{pop:,}" for pop in df['Population']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['Municipalities'],
                name='Municipalities',
                marker_color=['#ff7f0e', '#9467bd', '#bcbd22'],
                text=df['Municipalities'],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title='New Jersey Consolidation: Population and Government Structure',
            showlegend=False,
            height=500
        )
        
        # Key statistics cards
        stats_cards = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{target_region['population_2020'].sum():,}", className="text-primary"),
                        html.P("Current Population", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("3,610,711", className="text-success"),
                        html.P("Consolidated Population", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("3rd", className="text-warning"),
                        html.P("US City Rank", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("58th", className="text-info"),
                        html.P("World City Rank", className="card-text")
                    ])
                ])
            ], width=3)
        ], className="mb-4")
        
        return html.Div([
            stats_cards,
            dcc.Graph(figure=fig),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Population Analysis Insights"),
                    html.Ul([
                        html.Li("A consolidated Northern New Jersey would have over 3.6 million people"),
                        html.Li("This would make it larger than Chicago (2.7M) and Houston (2.3M)"),
                        html.Li("The current fragmented structure includes hundreds of separate municipalities"),
                        html.Li("Consolidation would create a single, more efficient government structure")
                    ])
                ])
            ])
        ])
    
    def create_rankings_tab(self):
        """Create the world rankings tab"""
        
        try:
            comparisons = pd.read_csv(self.data_dir / 'city_comparisons.csv')
        except FileNotFoundError:
            return dbc.Alert("Data not found. Please run data collection first.", color="warning")
        
        # Get top cities for comparison
        top_cities = comparisons.nlargest(15, 'population')
        
        # Add consolidated NJ
        nj_data = pd.DataFrame({
            'city': ['Greater Jersey City (Proposed)'],
            'country': ['USA'],
            'population': [3610711],
            'area_sq_km': [2000],
            'density_per_sq_km': [1805]
        })
        
        comparison_data = pd.concat([top_cities, nj_data], ignore_index=True)
        comparison_data = comparison_data.sort_values('population', ascending=True)
        
        # Create chart
        fig = go.Figure()
        
        colors = ['#2ca02c' if city == 'Greater Jersey City (Proposed)' 
                 else '#1f77b4' for city in comparison_data['city']]
        
        fig.add_trace(go.Bar(
            y=comparison_data['city'],
            x=comparison_data['population'],
            orientation='h',
            marker_color=colors,
            text=[f"{pop:,}" for pop in comparison_data['population']],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Population: %{x:,}<br>Country: %{customdata}<extra></extra>',
            customdata=comparison_data['country']
        ))
        
        fig.update_layout(
            title='World City Rankings: Where Greater Jersey City Would Stand',
            xaxis_title='Population',
            yaxis_title='City',
            height=600,
            showlegend=False
        )
        
        return html.Div([
            dcc.Graph(figure=fig),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Global Perspective"),
                    html.P([
                        "A consolidated Northern New Jersey would rank among the world's major cities, ",
                        "comparable to Madrid, Buenos Aires, and Toronto. This would give the region ",
                        "significant global influence and recognition."
                    ])
                ])
            ])
        ])
    
    def create_counties_tab(self):
        """Create the county breakdown tab"""
        
        try:
            municipalities = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
        except FileNotFoundError:
            return dbc.Alert("Data not found. Please run data collection first.", color="warning")
        
        target_region = municipalities[municipalities['in_target_region']]
        
        # County summary
        county_summary = target_region.groupby('county').agg({
            'population_2020': 'sum',
            'area_sq_miles': 'sum',
            'municipality': 'count'
        }).reset_index()
        
        county_summary.columns = ['County', 'Population', 'Area_Sq_Miles', 'Municipalities']
        county_summary['Population_Density'] = county_summary['Population'] / county_summary['Area_Sq_Miles']
        
        # Create charts
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Population by County', 'Municipalities by County', 
                          'Population Density', 'Area by County'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        county_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Population'],
                name='Population',
                marker_color=county_colors,
                text=[f"{pop:,}" for pop in county_summary['Population']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Municipalities'],
                name='Municipalities',
                marker_color=county_colors,
                text=county_summary['Municipalities'],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Population_Density'],
                name='Density',
                marker_color=county_colors,
                text=[f"{density:.0f}" for density in county_summary['Population_Density']],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Area_Sq_Miles'],
                name='Area',
                marker_color=county_colors,
                text=[f"{area:.1f}" for area in county_summary['Area_Sq_Miles']],
                textposition='auto'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Northern New Jersey Counties: Current Structure Analysis',
            showlegend=False,
            height=700
        )
        
        return html.Div([
            dcc.Graph(figure=fig),
            dbc.Card([
                dbc.CardBody([
                    html.H5("County Analysis"),
                    html.P([
                        "The five target counties show significant variation in population, ",
                        "area, and municipal structure. Bergen County has the most municipalities, ",
                        "while Hudson County is the most densely populated."
                    ])
                ])
            ])
        ])
    
    def create_economic_tab(self):
        """Create the economic impact tab"""
        
        # Create gauge charts for efficiency improvements
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Government Overhead Reduction', 'Infrastructure Efficiency',
                          'Public Services Enhancement', 'Administrative Cost Reduction'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Gauge 1: Government Overhead
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=30,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Government Overhead Reduction (%)"},
            delta={'reference': 0},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "#2ca02c"},
                   'steps': [{'range': [0, 20], 'color': "lightgray"},
                            {'range': [20, 30], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 30}}
        ), row=1, col=1)
        
        # Gauge 2: Infrastructure Efficiency
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=40,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Infrastructure Efficiency Improvement (%)"},
            delta={'reference': 0},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "#1f77b4"},
                   'steps': [{'range': [0, 25], 'color': "lightgray"},
                            {'range': [25, 40], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 40}}
        ), row=1, col=2)
        
        # Gauge 3: Public Services
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=25,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Public Services Enhancement (%)"},
            delta={'reference': 0},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "#ff7f0e"},
                   'steps': [{'range': [0, 15], 'color': "lightgray"},
                            {'range': [15, 25], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 25}}
        ), row=2, col=1)
        
        # Gauge 4: Administrative Costs
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=35,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Administrative Cost Reduction (%)"},
            delta={'reference': 0},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "#9467bd"},
                   'steps': [{'range': [0, 20], 'color': "lightgray"},
                            {'range': [20, 35], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 35}}
        ), row=2, col=2)
        
        fig.update_layout(
            title='Economic Impact of Consolidation: Efficiency Improvements',
            height=700
        )
        
        # Economic benefits card
        benefits_card = dbc.Card([
            dbc.CardBody([
                html.H5("Economic Benefits of Consolidation"),
                html.Ul([
                    html.Li("Estimated annual savings of $500 million"),
                    html.Li("Reduced government overhead and administrative costs"),
                    html.Li("Improved infrastructure project efficiency"),
                    html.Li("Enhanced public service delivery"),
                    html.Li("Streamlined planning and zoning processes"),
                    html.Li("Unified public transportation systems")
                ])
            ])
        ])
        
        return html.Div([
            dcc.Graph(figure=fig),
            benefits_card
        ])
    
    def create_sizes_tab(self):
        """Create the municipality sizes tab"""
        
        try:
            municipalities = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
        except FileNotFoundError:
            return dbc.Alert("Data not found. Please run data collection first.", color="warning")
        
        target_region = municipalities[municipalities['in_target_region']]
        
        # Create size categories
        target_region['size_category'] = pd.cut(
            target_region['population_2020'],
            bins=[0, 10000, 25000, 50000, 100000, float('inf')],
            labels=['Small (<10k)', 'Medium (10k-25k)', 'Large (25k-50k)', 
                   'Very Large (50k-100k)', 'Major (100k+)']
        )
        
        # Count by category
        size_distribution = target_region['size_category'].value_counts().sort_index()
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=size_distribution.index,
            values=size_distribution.values,
            hole=0.3,
            marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        )])
        
        fig.update_layout(
            title='Distribution of Municipality Sizes in Target Region',
            annotations=[dict(text='Municipalities<br>by Size', x=0.5, y=0.5, 
                            font_size=20, showarrow=False)]
        )
        
        # Size analysis card
        analysis_card = dbc.Card([
            dbc.CardBody([
                html.H5("Municipality Size Analysis"),
                html.P([
                    "The current municipal structure shows a wide range of municipality sizes, ",
                    "from small towns with fewer than 10,000 people to major cities with over 100,000. ",
                    "This fragmentation creates inefficiencies in service delivery and governance."
                ])
            ])
        ])
        
        return html.Div([
            dcc.Graph(figure=fig),
            analysis_card
        ])
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        self.app.run(debug=debug, port=port)

if __name__ == "__main__":
    dashboard = NJConsolidationDashboard()
    dashboard.run()
