"""
Simplified Data Collection Module for New Jersey Consolidation Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path

class NJDataCollector:
    """Collects and processes New Jersey municipal data"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Target counties for Northern New Jersey consolidation
        self.target_counties = ['Bergen', 'Essex', 'Hudson', 'Passaic', 'Union']
    
    def create_sample_data(self):
        """Create sample data for demonstration purposes"""
        
        # Create simple, working data
        municipalities_data = {
            'municipality': [
                'Newark', 'Jersey City', 'Paterson', 'Elizabeth', 'Edison',
                'Woodbridge', 'Lakewood', 'Toms River', 'Hamilton', 'Trenton',
                'Clifton', 'Camden', 'Brick', 'Cherry Hill', 'Passaic',
                'Union City', 'Bayonne', 'East Orange', 'Vineland', 'New Brunswick',
                'Bergenfield', 'Dumont', 'Fort Lee', 'Hackensack', 'Paramus',
                'Ridgewood', 'Teaneck', 'West New York', 'Hoboken', 'Secaucus',
                'Livingston', 'Maplewood', 'South Orange', 'West Orange', 'Montclair',
                'Bloomfield', 'Nutley', 'Belleville', 'Kearny', 'North Bergen'
            ],
            'county': [
                'Essex', 'Hudson', 'Passaic', 'Union', 'Middlesex',
                'Middlesex', 'Ocean', 'Ocean', 'Mercer', 'Mercer',
                'Passaic', 'Camden', 'Ocean', 'Camden', 'Passaic',
                'Hudson', 'Hudson', 'Essex', 'Cumberland', 'Middlesex',
                'Bergen', 'Bergen', 'Bergen', 'Bergen', 'Bergen',
                'Bergen', 'Bergen', 'Hudson', 'Hudson', 'Hudson',
                'Essex', 'Essex', 'Essex', 'Essex', 'Essex',
                'Essex', 'Essex', 'Essex', 'Hudson', 'Hudson'
            ],
            'population_2020': [
                311549, 292449, 159732, 137298, 107588,
                103639, 135158, 95838, 92089, 90632,
                90081, 71277, 76395, 74141, 70037,
                68400, 71026, 69012, 60780, 55641,
                28000, 18000, 40000, 46000, 27000,
                26000, 41000, 52000, 58000, 22000,
                31000, 25000, 18000, 48000, 41000,
                52000, 29000, 38000, 42000, 65000
            ],
            'area_sq_miles': [
                26.1, 14.8, 8.4, 12.3, 30.1,
                24.2, 24.9, 41.8, 40.1, 7.6,
                11.3, 9.1, 21.4, 14.2, 3.2,
                1.3, 5.8, 3.9, 69.4, 5.8,
                4.2, 2.1, 2.5, 4.3, 10.4,
                5.8, 6.2, 1.0, 2.0, 6.6,
                14.0, 3.9, 2.9, 12.1, 6.3,
                5.3, 3.4, 3.4, 8.7, 5.1
            ]
        }
        
        # Create DataFrame
        df = pd.DataFrame(municipalities_data)
        
        # Calculate population density
        df['population_density'] = df['population_2020'] / df['area_sq_miles']
        
        # Add calculated fields
        df['in_target_region'] = df['county'].isin(self.target_counties)
        
        # Save to CSV
        df.to_csv(self.data_dir / 'nj_municipalities.csv', index=False)
        
        return df
    
    def create_consolidation_scenarios(self):
        """Create data for different consolidation scenarios"""
        
        scenarios = {
            'scenario': [
                'Current (Fragmented)',
                '5-County Consolidation',
                '3-County Core (Bergen, Essex, Hudson)',
                'Hudson County Only',
                'Essex County Only',
                'Bergen County Only'
            ],
            'counties_included': [
                'All 21 counties',
                'Bergen, Essex, Hudson, Passaic, Union',
                'Bergen, Essex, Hudson',
                'Hudson',
                'Essex',
                'Bergen'
            ],
            'estimated_population': [
                9261699,  # Total NJ population
                3610711,  # 5-county consolidation from article
                2500000,  # Estimated 3-county core
                724854,   # Hudson County 2020 census
                863728,   # Essex County 2020 census
                955732    # Bergen County 2020 census
            ],
            'municipalities_count': [
                565,  # Total NJ municipalities
                200,  # Estimated municipalities in 5 counties
                120,  # Estimated municipalities in 3 counties
                12,   # Hudson County municipalities
                22,   # Essex County municipalities
                70    # Bergen County municipalities
            ],
            'us_city_rank': [
                'N/A',
                3,  # Would be 3rd largest US city
                5,  # Would be 5th largest US city
                15, # Would be 15th largest US city
                12, # Would be 12th largest US city
                10  # Would be 10th largest US city
            ],
            'world_city_rank': [
                'N/A',
                58,  # Would be 58th largest world city
                85,  # Would be 85th largest world city
                200, # Would be 200th largest world city
                180, # Would be 180th largest world city
                150  # Would be 150th largest world city
            ]
        }
        
        df = pd.DataFrame(scenarios)
        df.to_csv(self.data_dir / 'consolidation_scenarios.csv', index=False)
        
        return df
    
    def create_comparison_data(self):
        """Create data for comparing NJ consolidation to other major cities"""
        
        # Simple comparison data with exactly 20 cities
        comparison_data = {
            'city': [
                'New York City', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
                'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
                'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington'
            ],
            'country': [
                'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA',
                'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA'
            ],
            'population': [
                8336817, 3979576, 2693976, 2320268, 1608139,
                1584064, 1547253, 1423851, 1343573, 1035317,
                978908, 949611, 918915, 905748, 885708,
                873965, 887642, 749256, 715522, 705749
            ],
            'area_sq_km': [
                789, 1302, 606, 1701, 1344, 369, 1208, 964, 996, 467,
                826, 2265, 916, 577, 796, 121, 953, 370, 401, 177
            ],
            'density_per_sq_km': [
                10571, 3056, 4446, 1364, 1197, 4293, 1281, 1477, 1349, 2217,
                1185, 419, 1003, 1570, 1113, 7223, 932, 2025, 1784, 3987
            ]
        }
        
        # Add consolidated NJ to the data
        nj_data = pd.DataFrame({
            'city': ['Greater Jersey City (Proposed)'],
            'country': ['USA'],
            'population': [3610711],
            'area_sq_km': [2000],
            'density_per_sq_km': [1805]
        })
        
        # Combine and sort
        df = pd.DataFrame(comparison_data)
        df = pd.concat([df, nj_data], ignore_index=True)
        df.to_csv(self.data_dir / 'city_comparisons.csv', index=False)
        
        return df
    
    def create_economic_impact_data(self):
        """Create data showing potential economic benefits of consolidation"""
        
        economic_data = {
            'metric': [
                'Current Municipal Governments',
                'Consolidated Government',
                'Estimated Annual Savings',
                'Reduction in Government Overhead',
                'Improved Infrastructure Efficiency',
                'Enhanced Public Services',
                'Reduced Administrative Costs',
                'Streamlined Planning & Zoning',
                'Unified Public Transportation',
                'Coordinated Emergency Services'
            ],
            'current_value': [
                200, 1, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'consolidated_value': [
                1, 1, 500000000, 0.3, 0.4, 0.25, 0.35, 0.5, 0.6, 0.45
            ],
            'unit': [
                'count', 'count', 'USD', 'percentage', 'percentage',
                'percentage', 'percentage', 'percentage', 'percentage', 'percentage'
            ],
            'description': [
                'Number of separate municipal governments',
                'Single consolidated government entity',
                'Estimated annual cost savings from consolidation',
                'Reduction in government overhead costs',
                'Improvement in infrastructure project efficiency',
                'Enhancement in quality of public services',
                'Reduction in administrative and bureaucratic costs',
                'Streamlining of planning and zoning processes',
                'Unification of public transportation systems',
                'Better coordination of emergency services'
            ]
        }
        
        df = pd.DataFrame(economic_data)
        df.to_csv(self.data_dir / 'economic_impact.csv', index=False)
        
        return df
    
    def collect_all_data(self):
        """Collect all datasets for the analysis"""
        print("Creating sample municipal data...")
        municipalities = self.create_sample_data()
        
        print("Creating consolidation scenarios...")
        scenarios = self.create_consolidation_scenarios()
        
        print("Creating city comparison data...")
        comparisons = self.create_comparison_data()
        
        print("Creating economic impact data...")
        economic = self.create_economic_impact_data()
        
        print(f"Data collection complete! Files saved to {self.data_dir}")
        
        return {
            'municipalities': municipalities,
            'scenarios': scenarios,
            'comparisons': comparisons,
            'economic': economic
        }

if __name__ == "__main__":
    collector = NJDataCollector()
    data = collector.collect_all_data()
    
    print("\nData Summary:")
    for name, df in data.items():
        print(f"{name}: {len(df)} rows")
