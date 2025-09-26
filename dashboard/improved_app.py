"""
Improved Dashboard - Exact Copy of 8051 with Enhanced Municipal Boundaries

This is an exact copy of the enhanced dashboard (8051) but with improved
municipal boundary polygons instead of circles.
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
from enhanced_visualizations import EnhancedNJVisualizationCreator
from tiger_boundaries import TIGERBoundaryCreator

class ImprovedNJConsolidationDashboard:
    """Improved dashboard - exact copy of 8051 with enhanced municipal boundaries"""
    
    def __init__(self):
        # Use dark theme (same as 8051)
        self.app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.DARKLY]
        )
        self.data_dir = Path(__file__).parent.parent / 'data'
        
        # Initialize components
        self.data_collector = NJDataCollector()
        self.analyzer = NJConsolidationAnalyzer()
        self.viz_creator = EnhancedNJVisualizationCreator()
        self.tiger_creator = TIGERBoundaryCreator()
        
        # Load data
        self._load_data()
        
        # Setup layout and callbacks
        self.setup_layout()
        self.setup_callbacks()
    
    def _load_data(self):
        """Load all data and create visualizations"""
        # Collect data
        self.data = self.data_collector.collect_all_data()
        
        # Run analysis
        self.analyzer.load_data()
        self.analysis_results = {
            'population_analysis': self.analyzer.analyze_population_distribution(),
            'consolidation_impact': self.analyzer.analyze_consolidation_impact(),
            'efficiency_metrics': self.analyzer.analyze_efficiency_metrics(),
            'demographic_patterns': self.analyzer.analyze_demographic_patterns(),
            'key_findings': self.analyzer.generate_insights(),
            'efficiency_gains': {'efficiency_improvement': 0.35}
        }
        
        # Create visualizations
        self.claims_explanations = self.viz_creator.create_claims_explanation()
        self.tiger_creator.create_all_tiger_maps()
        
        # Load dataframes
        self.municipalities_df = self.data['municipalities']
        self.scenarios_df = self.data['scenarios']
        self.comparisons_df = self.data['comparisons']
        self.economic_df = self.data['economic']
        self.county_analysis_df = pd.read_csv(self.data_collector.data_dir / 'county_analysis.csv')
    
    def setup_layout(self):
        """Set up the dashboard layout (exact copy of 8051)"""
        
        # Header with dark theme
        header = dbc.NavbarSimple(
            brand="🏙️ New Jersey Consolidation Analysis",
            brand_href="#",
            color="dark",
            dark=True,
            className="mb-4",
            style={'background': 'linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%)'}
        )
        
        # Introduction card with dark theme
        intro_card = dbc.Card([
            dbc.CardBody([
                html.H4("The Case for Greater Jersey City", className="card-title text-light"),
                html.P([
                    "This dashboard explores the potential for consolidating Northern New Jersey's ",
                    "fragmented municipalities into a single, more efficient city. Based on the concept ",
                    "presented in ",
                    html.A("this article", href="https://papaghanoush.substack.com/p/new-jerseys-potential-and-a-plea", 
                          target="_blank", className="text-info"),
                    ", a consolidated Northern New Jersey would become the ",
                    html.Strong("3rd largest city in the United States"),
                    " with over 3.6 million people."
                ], className="text-light"),
                dbc.Alert([
                    html.H5("🎯 Key Insight", className="alert-heading"),
                    "If Bergen, Essex, Hudson, Passaic, and Union counties were consolidated into one city, "
                    "it would rank 58th globally, ahead of Madrid, Buenos Aires, and Toronto."
                ], color="info", className="border-info")
            ])
        ], className="bg-dark border-secondary")
        
        # Main content tabs
        tabs = dbc.Tabs([
            dbc.Tab(label="🗺️ Maps", tab_id="maps"),
            dbc.Tab(label="📊 Population Analysis", tab_id="population"),
            dbc.Tab(label="🌍 World Rankings", tab_id="rankings"),
            dbc.Tab(label="🏛️ County Breakdown", tab_id="counties"),
            dbc.Tab(label="💰 Economic Impact", tab_id="economic"),
            dbc.Tab(label="📋 Claims & Methodology", tab_id="claims")
        ], id="main-tabs", active_tab="maps", className="nav-pills")
        
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
                          target="_blank", className="text-info")
                ], className="text-muted small")
            ])
        ], className="bg-dark border-secondary mt-4")
        
        # Main layout
        self.app.layout = dbc.Container([
            header,
            intro_card,
            tabs,
            content,
            footer
        ], fluid=True, className="bg-dark")
    
    def setup_callbacks(self):
        """Set up dashboard callbacks (exact copy of 8051)"""
        
        @self.app.callback(
            Output("tab-content", "children"),
            Input("main-tabs", "active_tab")
        )
        def render_tab_content(active_tab):
            if active_tab == "maps":
                return self._render_maps_tab()
            elif active_tab == "population":
                return self._render_population_tab()
            elif active_tab == "rankings":
                return self._render_rankings_tab()
            elif active_tab == "counties":
                return self._render_counties_tab()
            elif active_tab == "economic":
                return self._render_economic_tab()
            elif active_tab == "claims":
                return self._render_claims_tab()
            return html.Div("Select a tab to view content.")
    
    def _render_maps_tab(self):
        """Render the maps tab with improved municipal boundaries"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("🗺️ Current Municipal Structure", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            html.P([
                                "Interactive map showing current municipal boundaries using ",
                                html.Strong("US Census Bureau TIGER/Line data", className="text-warning"),
                                " that trace actual waterways, coastlines, and natural boundaries. Each municipality is color-coded by county."
                            ], className="text-light"),
                            html.Iframe(
                                srcDoc=open(self.tiger_creator.output_dir / 'tiger_municipal_boundaries_map.html', 'r').read(),
                                style={"width": "100%", "height": "600px", "border": "none"}
                            )
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("🔄 Consolidation Scenarios", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            html.P([
                                "Map showing proposed consolidation scenarios using ",
                                html.Strong("US Census Bureau TIGER/Line county boundaries", className="text-warning"),
                                " that follow actual geographic features and interactive toggles."
                            ], className="text-light"),
                            html.Iframe(
                                srcDoc=open(self.tiger_creator.output_dir / 'tiger_consolidation_map.html', 'r').read(),
                                style={"width": "100%", "height": "600px", "border": "none"}
                            )
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=6)
            ])
        ], fluid=True)
    
    def _render_population_tab(self):
        """Render the population analysis tab"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("📊 Population Comparison", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            dcc.Graph(figure=self.viz_creator.create_dark_population_chart())
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=12)
            ])
        ], fluid=True)
    
    def _render_rankings_tab(self):
        """Render the world rankings tab"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("🌍 World City Rankings", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            dcc.Graph(figure=self.viz_creator.create_dark_world_ranking_chart())
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=12)
            ])
        ], fluid=True)
    
    def _render_counties_tab(self):
        """Render the county breakdown tab"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("🏛️ County Analysis", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            dcc.Graph(figure=self._create_county_chart())
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=12)
            ])
        ], fluid=True)
    
    def _render_economic_tab(self):
        """Render the economic impact tab"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("💰 Economic Impact", className="text-light mb-0")
                        ], className="bg-secondary"),
                        dbc.CardBody([
                            dcc.Graph(figure=self._create_economic_chart())
                        ])
                    ], className="bg-dark border-secondary mb-4")
                ], md=12)
            ])
        ], fluid=True)
    
    def _render_claims_tab(self):
        """Render the claims and methodology tab"""
        cards = []
        for key, claim_data in self.claims_explanations.items():
            cards.append(
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(claim_data['claim'], className="text-light mb-0")
                    ], className="bg-secondary"),
                    dbc.CardBody([
                        html.P([
                            html.Strong("Methodology: ", className="text-info"),
                            claim_data['methodology']
                        ], className="text-light"),
                        html.P([
                            html.Strong("Data Source: ", className="text-info"),
                            claim_data['data_source']
                        ], className="text-light"),
                        html.P([
                            html.Strong("Validation: ", className="text-info"),
                            claim_data['validation']
                        ], className="text-light"),
                        html.P([
                            html.Strong("Confidence: ", className="text-info"),
                            claim_data['confidence']
                        ], className="text-light")
                    ])
                ], className="bg-dark border-secondary mb-3")
            )
        
        return dbc.Container(cards, fluid=True)
    
    def _create_county_chart(self):
        """Create county analysis chart"""
        county_data = self.county_analysis_df.sort_values('total_population', ascending=True)
        
        fig = px.bar(
            county_data,
            x='total_population',
            y='county',
            orientation='h',
            title='Population by County',
            labels={'total_population': 'Population', 'county': 'County'},
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _create_economic_chart(self):
        """Create economic impact chart"""
        savings_data = self.economic_df[self.economic_df['metric'] == 'Estimated Annual Savings']
        if not savings_data.empty:
            fig = px.bar(
                x=['Current', 'Consolidated'],
                y=[savings_data['current_value'].iloc[0], savings_data['consolidated_value'].iloc[0]],
                title='Economic Impact of Consolidation',
                labels={'x': 'Scenario', 'y': 'Annual Cost (Millions $)'},
                template='plotly_dark'
            )
        else:
            fig = px.bar(
                x=['Current', 'Consolidated'],
                y=[500, 0],
                title='Economic Impact of Consolidation',
                labels={'x': 'Scenario', 'y': 'Annual Cost (Millions $)'},
                template='plotly_dark'
            )
        
        fig.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def run(self, debug=True, port=8053):
        """Run the improved dashboard"""
        self.app.run(debug=debug, port=port)

if __name__ == "__main__":
    dashboard = ImprovedNJConsolidationDashboard()
    dashboard.run()