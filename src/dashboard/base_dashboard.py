"""
Base dashboard class for the New Jersey Municipal Consolidation Analysis.
Provides common functionality for all dashboard implementations.
"""

import logging
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from typing import Dict, Any

from config.settings import (
    DASHBOARD_PORTS, COUNTY_COLORS, POPULATION_DATA, ECONOMIC_IMPACT,
    CONSOLIDATION_SCENARIOS
)

logger = logging.getLogger(__name__)


class BaseNJConsolidationDashboard:
    """Base class for New Jersey consolidation analysis dashboards."""
    
    def __init__(self, port: int = 8051):
        self.port = port
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        
        # Initialize data
        self.data = {}
        self.analysis_results = {}
        self.claims_explanations = {}
        
        # Setup layout and callbacks
        self._setup_layout()
        self._setup_callbacks()
        
        logger.info(f"Base dashboard initialized on port {port}")
    
    def _load_data(self):
        """Load all required data. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _load_data")
    
    def _setup_layout(self):
        """Setup the dashboard layout."""
        self.app.layout = dbc.Container([
            html.H1("Greater Jersey City: Consolidation Analysis", 
                   className="my-4 text-center text-primary"),
            html.P("Exploring the potential for municipal consolidation in Northern New Jersey.", 
                   className="lead text-center text-light"),

            dbc.Tabs([
                dbc.Tab(label="Overview", tab_id="overview-tab", children=[
                    self._create_overview_tab()
                ]),
                
                dbc.Tab(label="Interactive Maps", tab_id="maps-tab", children=[
                    self._create_maps_tab()
                ]),
                
                dbc.Tab(label="Population & Rankings", tab_id="pop-rank-tab", children=[
                    self._create_population_tab()
                ]),
                
                dbc.Tab(label="County Analysis", tab_id="county-tab", children=[
                    self._create_county_tab()
                ]),
                
                dbc.Tab(label="Economic Impact", tab_id="economic-tab", children=[
                    self._create_economic_tab()
                ]),
                
                dbc.Tab(label="Methodology & Claims", tab_id="claims-tab", children=[
                    self._create_claims_tab()
                ]),
            ])
        ], fluid=True, className="bg-dark")
    
    def _create_overview_tab(self):
        """Create the overview tab content."""
        return html.Div(className="my-4", children=[
            html.H2("Key Insights", className="text-light mb-4"),
            dbc.Row([
                dbc.Col(self._create_insight_card("Consolidated Population", 
                                               f"{POPULATION_DATA['consolidated_population']:,}", 
                                               " people", "primary"), md=4),
                dbc.Col(self._create_insight_card("US City Rank", 
                                               f"{POPULATION_DATA['us_city_rank']}rd", 
                                               "", "info"), md=4),
                dbc.Col(self._create_insight_card("Global City Rank", 
                                               f"{POPULATION_DATA['world_city_rank']}th", 
                                               "", "success"), md=4),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(self._create_insight_card("Annual Savings", 
                                               f"${ECONOMIC_IMPACT['annual_savings_millions']}M", 
                                               "", "warning"), md=4),
                dbc.Col(self._create_insight_card("Municipalities Reduced", 
                                               ECONOMIC_IMPACT['government_reduction'], 
                                               "", "danger"), md=4),
                dbc.Col(self._create_insight_card("Efficiency Gains", 
                                               f"{ECONOMIC_IMPACT['efficiency_improvement_percent']}%", 
                                               "", "secondary"), md=4),
            ]),
        ])
    
    def _create_maps_tab(self):
        """Create the maps tab content."""
        return html.Div(className="my-4", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("Current Municipal Structure", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            self._create_map_iframe('tiger_municipal_boundaries_map.html')
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("Consolidation Scenarios", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            self._create_map_iframe('tiger_consolidation_map.html')
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=6)
            ])
        ])
    
    def _create_map_iframe(self, filename: str):
        """Create an iframe for displaying maps."""
        map_path = Path("visualizations") / filename
        if map_path.exists():
            with open(map_path, 'r') as f:
                map_content = f.read()
            return html.Iframe(
                srcDoc=map_content,
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        else:
            return html.Div([
                html.P(f"Map file {filename} not found.", className="text-warning"),
                html.P("Please ensure the TIGER/Line data processing has completed successfully.", 
                       className="text-muted")
            ])
    
    def _create_population_tab(self):
        """Create the population analysis tab content."""
        return html.Div(className="my-4", children=[
            html.H2("Population Analysis", className="text-light mb-4"),
            dcc.Graph(figure=self._create_population_chart()),
            
            html.H2("World City Ranking", className="text-light mt-5 mb-4"),
            dcc.Graph(figure=self._create_world_ranking_chart()),
        ])
    
    def _create_county_tab(self):
        """Create the county analysis tab content."""
        return html.Div(className="my-4", children=[
            html.H2("County Breakdown", className="text-light mb-4"),
            dcc.Graph(figure=self._create_county_analysis_chart()),
        ])
    
    def _create_economic_tab(self):
        """Create the economic impact tab content."""
        return html.Div(className="my-4", children=[
            html.H2("Economic Benefits of Consolidation", className="text-light mb-4"),
            dcc.Graph(figure=self._create_economic_impact_chart()),
        ])
    
    def _create_claims_tab(self):
        """Create the claims explanation tab content."""
        return html.Div(className="my-4", children=[
            html.H2("Detailed Explanation of Claims", className="text-light mb-4"),
            self._render_claims_explanation()
        ])
    
    def _create_insight_card(self, title: str, value: str, unit: str, color: str):
        """Create a styled insight card."""
        return dbc.Card([
            dbc.CardBody([
                html.H6(title, className="card-subtitle text-muted"),
                html.H3(f"{value}{unit}", className=f"card-text text-{color}")
            ])
        ], className="mb-3 bg-secondary text-white border-0")
    
    def _create_population_chart(self):
        """Create population comparison chart."""
        # This should be implemented by subclasses with actual data
        fig = go.Figure()
        fig.update_layout(
            title="Population Comparison (Dark Theme)",
            template="plotly_dark",
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _create_world_ranking_chart(self):
        """Create world city ranking chart."""
        # This should be implemented by subclasses with actual data
        fig = go.Figure()
        fig.update_layout(
            title="World City Ranking (Dark Theme)",
            template="plotly_dark",
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _create_county_analysis_chart(self):
        """Create county analysis chart."""
        # This should be implemented by subclasses with actual data
        fig = go.Figure()
        fig.update_layout(
            title="County Analysis (Dark Theme)",
            template="plotly_dark",
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _create_economic_impact_chart(self):
        """Create economic impact chart."""
        # This should be implemented by subclasses with actual data
        fig = go.Figure()
        fig.update_layout(
            title="Economic Impact (Dark Theme)",
            template="plotly_dark",
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _render_claims_explanation(self):
        """Render claims explanations."""
        if not self.claims_explanations:
            return html.Div([
                html.P("Claims explanations not available.", className="text-warning")
            ])
        
        cards = []
        for key, claim_data in self.claims_explanations.items():
            cards.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H4(claim_data['claim'], className="card-title text-primary"),
                        html.P(f"Methodology: {claim_data['methodology']}", className="card-text text-light"),
                        html.P(f"Data Source: {claim_data['data_source']}", className="card-text text-light"),
                        html.P(f"Validation: {claim_data['validation']}", className="card-text text-light"),
                        html.P(f"Confidence: {claim_data['confidence']}", className="card-text text-light"),
                    ]),
                    className="mb-3 bg-secondary text-white border-0"
                )
            )
        return html.Div(cards)
    
    def _setup_callbacks(self):
        """Setup dashboard callbacks."""
        # Base implementation - can be extended by subclasses
        pass
    
    def run(self, debug: bool = True):
        """Run the dashboard."""
        logger.info(f"Starting dashboard on port {self.port}")
        self.app.run(debug=debug, port=self.port)
