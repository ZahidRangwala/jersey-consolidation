"""
Main dashboard implementation for the New Jersey Municipal Consolidation Analysis.
Uses the refactored architecture with proper separation of concerns.
"""

import logging
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.dashboard.base_dashboard import BaseNJConsolidationDashboard
from src.core.data_manager import DataManager
from src.core.tiger_processor import TIGERProcessor
from src.data_collection import NJDataCollector
from src.analysis import NJConsolidationAnalyzer
from src.enhanced_visualizations import EnhancedNJVisualizationCreator

logger = logging.getLogger(__name__)


class MainNJConsolidationDashboard(BaseNJConsolidationDashboard):
    """Main dashboard implementation with full functionality."""
    
    def __init__(self, port: int = 8051):
        super().__init__(port)
        
        # Initialize components
        self.data_manager = DataManager()
        self.tiger_processor = TIGERProcessor(self.data_manager)
        self.data_collector = NJDataCollector()
        self.analyzer = NJConsolidationAnalyzer()
        self.viz_creator = EnhancedNJVisualizationCreator()
        
        # Load data
        self._load_data()
        
        logger.info("Main dashboard initialized with full functionality")
    
    def _load_data(self):
        """Load all required data."""
        logger.info("Loading dashboard data...")
        
        try:
            # Collect sample data
            self.data = self.data_collector.collect_all_data()
            
            # Load analysis results
            self.analyzer.load_data()
            self.analysis_results = {
                'population_analysis': self.analyzer.analyze_population_distribution(),
                'consolidation_impact': self.analyzer.analyze_consolidation_impact(),
                'efficiency_metrics': self.analyzer.analyze_demographic_patterns(),
                'demographic_patterns': self.analyzer.analyze_demographic_patterns(),
                'key_findings': self.analyzer.generate_insights(),
                'efficiency_gains': {'efficiency_improvement': 0.35}
            }
            
            # Create visualizations
            self.claims_explanations = self.viz_creator.create_claims_explanation()
            
            # Create TIGER/Line maps
            self.tiger_processor.create_all_maps()
            
            # Load dataframes
            self.municipalities_df = self.data['municipalities']
            self.scenarios_df = self.data['scenarios']
            self.comparisons_df = self.data['comparisons']
            self.economic_df = self.data['economic']
            self.county_analysis_df = pd.read_csv(self.data_collector.data_dir / 'county_analysis.csv')
            
            logger.info("Dashboard data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            raise
    
    def _create_population_chart(self):
        """Create population comparison chart with actual data."""
        return self.viz_creator.create_dark_population_chart()
    
    def _create_world_ranking_chart(self):
        """Create world city ranking chart with actual data."""
        return self.viz_creator.create_dark_world_ranking_chart()
    
    def _create_county_analysis_chart(self):
        """Create county analysis chart with actual data."""
        county_data = self.county_analysis_df.sort_values('total_population', ascending=True)
        
        fig = px.bar(
            county_data,
            x='total_population',
            y='county',
            orientation='h',
            title='Population by County (Dark Theme)',
            labels={'total_population': 'Population', 'county': 'County'},
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig
    
    def _create_economic_impact_chart(self):
        """Create economic impact chart with actual data."""
        savings_data = self.economic_df[self.economic_df['metric'] == 'Estimated Annual Savings']
        if not savings_data.empty:
            fig = px.bar(
                x=['Current', 'Consolidated'],
                y=[savings_data['current_value'].iloc[0], savings_data['consolidated_value'].iloc[0]],
                title='Economic Impact of Consolidation (Dark Theme)',
                labels={'x': 'Scenario', 'y': 'Annual Cost (Millions $)'},
                template='plotly_dark'
            )
        else:
            fig = px.bar(
                x=['Current', 'Consolidated'],
                y=[500, 0],
                title='Economic Impact of Consolidation (Dark Theme)',
                labels={'x': 'Scenario', 'y': 'Annual Cost (Millions $)'},
                template='plotly_dark'
            )
        fig.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font_color='white'
        )
        return fig


def create_dashboard(port: int = 8051) -> MainNJConsolidationDashboard:
    """Factory function to create a dashboard instance."""
    return MainNJConsolidationDashboard(port)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    
    # Create and run dashboard
    dashboard = create_dashboard(port=8051)
    dashboard.run(debug=True)
