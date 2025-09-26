"""
Analysis Module for New Jersey Consolidation Project

This module performs various analyses on the collected data to support
the visualization and insights about municipal consolidation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

class NJConsolidationAnalyzer:
    """Analyzes New Jersey municipal data for consolidation insights"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        
    def load_data(self):
        """Load all collected datasets"""
        try:
            self.municipalities = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
            self.scenarios = pd.read_csv(self.data_dir / 'consolidation_scenarios.csv')
            self.comparisons = pd.read_csv(self.data_dir / 'city_comparisons.csv')
            self.economic = pd.read_csv(self.data_dir / 'economic_impact.csv')
            return True
        except FileNotFoundError as e:
            print(f"Data files not found: {e}")
            return False
    
    def analyze_population_distribution(self):
        """Analyze population distribution across municipalities"""
        
        # Target region analysis
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
        analysis = {
            'total_municipalities': len(self.municipalities),
            'target_region_municipalities': len(target_region),
            'total_population': self.municipalities['population_2020'].sum(),
            'target_region_population': target_region['population_2020'].sum(),
            'largest_municipality': target_region.loc[target_region['population_2020'].idxmax(), 'municipality'],
            'largest_population': target_region['population_2020'].max(),
            'smallest_municipality': target_region.loc[target_region['population_2020'].idxmin(), 'municipality'],
            'smallest_population': target_region['population_2020'].min(),
            'average_population': target_region['population_2020'].mean(),
            'median_population': target_region['population_2020'].median()
        }
        
        # County breakdown
        county_analysis = target_region.groupby('county').agg({
            'population_2020': ['sum', 'count', 'mean'],
            'area_sq_miles': 'sum',
            'population_density': 'mean'
        }).round(2)
        
        county_analysis.columns = ['total_population', 'municipality_count', 'avg_population', 'total_area', 'avg_density']
        county_analysis = county_analysis.reset_index()
        
        return {
            'summary': analysis,
            'county_breakdown': county_analysis
        }
    
    def analyze_consolidation_impact(self):
        """Analyze the impact of different consolidation scenarios"""
        
        # Current vs consolidated comparison
        current_pop = self.municipalities[self.municipalities['in_target_region']]['population_2020'].sum()
        consolidated_pop = self.scenarios[self.scenarios['scenario'] == '5-County Consolidation']['estimated_population'].iloc[0]
        
        # Calculate rankings
        us_rankings = self.comparisons[self.comparisons['country'] == 'USA'].copy()
        us_rankings = us_rankings.sort_values('population', ascending=False).reset_index(drop=True)
        us_rankings['us_rank'] = range(1, len(us_rankings) + 1)
        
        # Find where consolidated NJ would rank
        nj_rank = len(us_rankings[us_rankings['population'] > consolidated_pop]) + 1
        
        # World rankings
        world_rankings = self.comparisons.sort_values('population', ascending=False).reset_index(drop=True)
        world_rankings['world_rank'] = range(1, len(world_rankings) + 1)
        
        nj_world_rank = len(world_rankings[world_rankings['population'] > consolidated_pop]) + 1
        
        analysis = {
            'current_population': current_pop,
            'consolidated_population': consolidated_pop,
            'population_difference': consolidated_pop - current_pop,
            'us_city_rank': nj_rank,
            'world_city_rank': nj_world_rank,
            'would_be_larger_than': us_rankings[us_rankings['population'] < consolidated_pop]['city'].head(5).tolist(),
            'would_be_smaller_than': us_rankings[us_rankings['population'] > consolidated_pop]['city'].head(5).tolist()
        }
        
        return analysis
    
    def analyze_efficiency_metrics(self):
        """Analyze potential efficiency gains from consolidation"""
        
        # Calculate current inefficiencies
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
        # Government overhead (estimated based on number of municipalities)
        current_governments = len(target_region)
        estimated_overhead_per_municipality = 2000000  # $2M per municipality annually
        
        current_total_overhead = current_governments * estimated_overhead_per_municipality
        consolidated_overhead = estimated_overhead_per_municipality * 3  # 3x for larger consolidated government
        
        # Infrastructure efficiency
        current_infrastructure_score = 0.6  # Current efficiency
        consolidated_infrastructure_score = 0.85  # Improved efficiency
        
        # Public services efficiency
        current_services_score = 0.7
        consolidated_services_score = 0.9
        
        analysis = {
            'current_governments': current_governments,
            'consolidated_governments': 1,
            'government_reduction': current_governments - 1,
            'current_overhead_cost': current_total_overhead,
            'consolidated_overhead_cost': consolidated_overhead,
            'overhead_savings': current_total_overhead - consolidated_overhead,
            'infrastructure_efficiency_gain': consolidated_infrastructure_score - current_infrastructure_score,
            'services_efficiency_gain': consolidated_services_score - current_services_score,
            'total_annual_savings': self.economic[self.economic['metric'] == 'Estimated Annual Savings']['consolidated_value'].iloc[0]
        }
        
        return analysis
    
    def analyze_demographic_patterns(self):
        """Analyze demographic patterns across the target region"""
        
        target_region = self.municipalities[self.municipalities['in_target_region']]
        
        # Population density analysis
        density_analysis = {
            'highest_density': target_region.loc[target_region['population_density'].idxmax()].to_dict(),
            'lowest_density': target_region.loc[target_region['population_density'].idxmin()].to_dict(),
            'average_density': target_region['population_density'].mean(),
            'density_std': target_region['population_density'].std()
        }
        
        # Size distribution
        size_categories = pd.cut(target_region['population_2020'], 
                               bins=[0, 10000, 50000, 100000, float('inf')],
                               labels=['Small (<10k)', 'Medium (10k-50k)', 'Large (50k-100k)', 'Very Large (100k+)'])
        
        size_distribution = size_categories.value_counts().to_dict()
        
        # County analysis
        county_stats = target_region.groupby('county').agg({
            'population_2020': ['sum', 'mean', 'std'],
            'area_sq_miles': 'sum',
            'population_density': ['mean', 'std']
        }).round(2)
        
        return {
            'density_analysis': density_analysis,
            'size_distribution': size_distribution,
            'county_statistics': county_stats
        }
    
    def generate_insights(self):
        """Generate key insights from all analyses"""
        
        if not self.load_data():
            return None
        
        population_analysis = self.analyze_population_distribution()
        consolidation_analysis = self.analyze_consolidation_impact()
        efficiency_analysis = self.analyze_efficiency_metrics()
        demographic_analysis = self.analyze_demographic_patterns()
        
        insights = {
            'key_findings': [
                f"A consolidated Northern New Jersey would have {consolidation_analysis['consolidated_population']:,} people",
                f"This would make it the {consolidation_analysis['us_city_rank']}rd largest city in the United States",
                f"Globally, it would rank {consolidation_analysis['world_city_rank']}th among world cities",
                f"Consolidation could save approximately ${efficiency_analysis['total_annual_savings']:,} annually",
                f"Current fragmentation includes {efficiency_analysis['current_governments']} separate municipal governments",
                f"The largest municipality is {population_analysis['summary']['largest_municipality']} with {population_analysis['summary']['largest_population']:,} people",
                f"Average municipality size is {population_analysis['summary']['average_population']:,.0f} people"
            ],
            'comparisons': {
                'larger_than': consolidation_analysis['would_be_larger_than'],
                'smaller_than': consolidation_analysis['would_be_smaller_than']
            },
            'efficiency_gains': {
                'government_reduction': efficiency_analysis['government_reduction'],
                'overhead_savings': efficiency_analysis['overhead_savings'],
                'infrastructure_improvement': efficiency_analysis['infrastructure_efficiency_gain'],
                'services_improvement': efficiency_analysis['services_efficiency_gain']
            }
        }
        
        return insights
    
    def save_analysis_results(self, output_dir="data"):
        """Save analysis results to files"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        insights = self.generate_insights()
        
        if insights:
            # Save insights as JSON
            with open(output_path / 'analysis_insights.json', 'w') as f:
                json.dump(insights, f, indent=2)
            
            # Save detailed analysis results
            population_analysis = self.analyze_population_distribution()
            consolidation_analysis = self.analyze_consolidation_impact()
            efficiency_analysis = self.analyze_efficiency_metrics()
            demographic_analysis = self.analyze_demographic_patterns()
            
            # Save county breakdown
            population_analysis['county_breakdown'].to_csv(output_path / 'county_analysis.csv', index=False)
            
            print(f"Analysis results saved to {output_path}")
            return True
        
        return False

if __name__ == "__main__":
    analyzer = NJConsolidationAnalyzer()
    
    if analyzer.save_analysis_results():
        print("Analysis complete!")
        
        # Print key insights
        insights = analyzer.generate_insights()
        if insights:
            print("\nKey Insights:")
            for finding in insights['key_findings']:
                print(f"• {finding}")
    else:
        print("Analysis failed - please run data collection first")
