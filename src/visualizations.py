"""
Visualization Module for New Jersey Consolidation Project

This module creates various visualizations to illustrate the potential
benefits and impacts of municipal consolidation in Northern New Jersey.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from pathlib import Path
import json

class NJVisualizationCreator:
    """Creates visualizations for New Jersey consolidation analysis"""
    
    def __init__(self, data_dir="data", output_dir="visualizations"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load data
        self.load_data()
        
        # Color schemes
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#bcbd22',
            'dark': '#17becf'
        }
        
        # County colors for consistency
        self.county_colors = {
            'Bergen': '#1f77b4',
            'Essex': '#ff7f0e', 
            'Hudson': '#2ca02c',
            'Passaic': '#d62728',
            'Union': '#9467bd'
        }
    
    def load_data(self):
        """Load all datasets"""
        try:
            self.municipalities = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
            self.scenarios = pd.read_csv(self.data_dir / 'consolidation_scenarios.csv')
            self.comparisons = pd.read_csv(self.data_dir / 'city_comparisons.csv')
            self.economic = pd.read_csv(self.data_dir / 'economic_impact.csv')
            
            # Load analysis results if available
            try:
                with open(self.data_dir / 'analysis_insights.json', 'r') as f:
                    self.insights = json.load(f)
            except FileNotFoundError:
                self.insights = None
                
            return True
        except FileNotFoundError as e:
            print(f"Data files not found: {e}")
            return False
    
    def create_population_comparison_chart(self):
        """Create a chart comparing current vs consolidated population scenarios"""
        
        # Filter to target region
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
        # Create comparison data
        comparison_data = {
            'Scenario': ['Current (Fragmented)', '5-County Consolidation', '3-County Core'],
            'Population': [
                target_region['population_2020'].sum(),
                3610711,  # From article
                2500000   # Estimated
            ],
            'Municipalities': [
                len(target_region),
                1,
                1
            ],
            'US_Rank': ['N/A', 3, 5],
            'World_Rank': ['N/A', 58, 85]
        }
        
        df = pd.DataFrame(comparison_data)
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Population Comparison', 'Municipalities Count'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Population chart
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['Population'],
                name='Population',
                marker_color=[self.colors['primary'], self.colors['success'], self.colors['warning']],
                text=[f"{pop:,}" for pop in df['Population']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # Municipalities chart
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['Municipalities'],
                name='Municipalities',
                marker_color=[self.colors['secondary'], self.colors['info'], self.colors['light']],
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
        
        fig.update_xaxes(title_text="Scenario", row=1, col=1)
        fig.update_xaxes(title_text="Scenario", row=1, col=2)
        fig.update_yaxes(title_text="Population", row=1, col=1)
        fig.update_yaxes(title_text="Number of Municipalities", row=1, col=2)
        
        # Save the chart
        fig.write_html(self.output_dir / 'population_comparison.html')
        try:
            fig.write_image(self.output_dir / 'population_comparison.png', width=1200, height=500)
        except Exception as e:
            print(f"Note: Could not save PNG image: {e}")
        
        return fig
    
    def create_world_city_ranking_chart(self):
        """Create a chart showing where consolidated NJ would rank among world cities"""
        
        # Get top cities for comparison
        top_cities = self.comparisons.nlargest(20, 'population')
        
        # Add consolidated NJ to the data
        nj_data = pd.DataFrame({
            'city': ['Greater Jersey City (Proposed)'],
            'country': ['USA'],
            'population': [3610711],
            'area_sq_km': [2000],  # Estimated
            'density_per_sq_km': [1805]  # Estimated
        })
        
        # Combine and sort
        comparison_data = pd.concat([top_cities, nj_data], ignore_index=True)
        comparison_data = comparison_data.sort_values('population', ascending=True)
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        # Color bars differently for NJ
        colors = [self.colors['success'] if city == 'Greater Jersey City (Proposed)' 
                 else self.colors['primary'] for city in comparison_data['city']]
        
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
            height=800,
            showlegend=False
        )
        
        # Save the chart
        fig.write_html(self.output_dir / 'world_city_ranking.html')
        try:
            fig.write_image(self.output_dir / 'world_city_ranking.png', width=1000, height=800)
        except Exception as e:
            print(f"Note: Could not save PNG image: {e}")
        
        return fig
    
    def create_county_analysis_chart(self):
        """Create charts analyzing population distribution by county"""
        
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
        # County summary
        county_summary = target_region.groupby('county').agg({
            'population_2020': 'sum',
            'area_sq_miles': 'sum',
            'municipality': 'count'
        }).reset_index()
        
        county_summary.columns = ['County', 'Population', 'Area_Sq_Miles', 'Municipalities']
        county_summary['Population_Density'] = county_summary['Population'] / county_summary['Area_Sq_Miles']
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Population by County', 'Municipalities by County', 
                          'Population Density', 'Area by County'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Population chart
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Population'],
                name='Population',
                marker_color=[self.county_colors.get(county, self.colors['primary']) 
                            for county in county_summary['County']],
                text=[f"{pop:,}" for pop in county_summary['Population']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # Municipalities chart
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Municipalities'],
                name='Municipalities',
                marker_color=[self.county_colors.get(county, self.colors['secondary']) 
                            for county in county_summary['County']],
                text=county_summary['Municipalities'],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        # Density chart
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Population_Density'],
                name='Density',
                marker_color=[self.county_colors.get(county, self.colors['warning']) 
                            for county in county_summary['County']],
                text=[f"{density:.0f}" for density in county_summary['Population_Density']],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        # Area chart
        fig.add_trace(
            go.Bar(
                x=county_summary['County'],
                y=county_summary['Area_Sq_Miles'],
                name='Area',
                marker_color=[self.county_colors.get(county, self.colors['info']) 
                            for county in county_summary['County']],
                text=[f"{area:.1f}" for area in county_summary['Area_Sq_Miles']],
                textposition='auto'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Northern New Jersey Counties: Current Structure Analysis',
            showlegend=False,
            height=800
        )
        
        # Save the chart
        fig.write_html(self.output_dir / 'county_analysis.html')
        try:
            fig.write_image(self.output_dir / 'county_analysis.png', width=1200, height=800)
        except Exception as e:
            print(f"Note: Could not save PNG image: {e}")
        
        return fig
    
    def create_economic_impact_chart(self):
        """Create charts showing potential economic benefits of consolidation"""
        
        # Economic impact data
        economic_data = self.economic[self.economic['unit'] == 'percentage'].copy()
        
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
                   'bar': {'color': self.colors['success']},
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
                   'bar': {'color': self.colors['primary']},
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
                   'bar': {'color': self.colors['warning']},
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
                   'bar': {'color': self.colors['info']},
                   'steps': [{'range': [0, 20], 'color': "lightgray"},
                            {'range': [20, 35], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 35}}
        ), row=2, col=2)
        
        fig.update_layout(
            title='Economic Impact of Consolidation: Efficiency Improvements',
            height=800
        )
        
        # Save the chart
        fig.write_html(self.output_dir / 'economic_impact.html')
        try:
            fig.write_image(self.output_dir / 'economic_impact.png', width=1200, height=800)
        except Exception as e:
            print(f"Note: Could not save PNG image: {e}")
        
        return fig
    
    def create_municipality_size_distribution(self):
        """Create a chart showing the distribution of municipality sizes"""
        
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
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
            marker_colors=[self.colors['primary'], self.colors['secondary'], 
                          self.colors['success'], self.colors['warning'], self.colors['info']]
        )])
        
        fig.update_layout(
            title='Distribution of Municipality Sizes in Target Region',
            annotations=[dict(text='Municipalities<br>by Size', x=0.5, y=0.5, 
                            font_size=20, showarrow=False)]
        )
        
        # Save the chart
        fig.write_html(self.output_dir / 'municipality_size_distribution.html')
        try:
            fig.write_image(self.output_dir / 'municipality_size_distribution.png', width=800, height=600)
        except Exception as e:
            print(f"Note: Could not save PNG image: {e}")
        
        return fig
    
    def create_all_visualizations(self):
        """Create all visualizations and save them"""
        
        if not self.load_data():
            print("Failed to load data. Please run data collection first.")
            return False
        
        print("Creating population comparison chart...")
        self.create_population_comparison_chart()
        
        print("Creating world city ranking chart...")
        self.create_world_city_ranking_chart()
        
        print("Creating county analysis chart...")
        self.create_county_analysis_chart()
        
        print("Creating economic impact chart...")
        self.create_economic_impact_chart()
        
        print("Creating municipality size distribution chart...")
        self.create_municipality_size_distribution()
        
        print(f"All visualizations saved to {self.output_dir}")
        return True

if __name__ == "__main__":
    visualizer = NJVisualizationCreator()
    visualizer.create_all_visualizations()
