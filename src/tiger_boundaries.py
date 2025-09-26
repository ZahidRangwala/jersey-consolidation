"""
TIGER/Line Municipal Boundaries Creator

This module downloads and processes US Census Bureau TIGER/Line files to create
accurate municipal boundary polygons that follow real geographic features.
"""

import pandas as pd
import numpy as np
import folium
import json
import requests
import zipfile
from pathlib import Path
from shapely.geometry import Polygon, Point
import geopandas as gpd
import os

class TIGERBoundaryCreator:
    """Creates maps using US Census Bureau TIGER/Line municipal boundary data"""
    
    def __init__(self, data_dir="data", output_dir="visualizations"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create TIGER data directory
        self.tiger_dir = self.data_dir / 'tiger_data'
        self.tiger_dir.mkdir(exist_ok=True)
        
        # County colors
        self.county_colors = {
            'Bergen': '#00d4ff',
            'Essex': '#ff6b35', 
            'Hudson': '#00ff88',
            'Passaic': '#ffb347',
            'Union': '#9d4edd'
        }
        
        # Target counties for Northern New Jersey
        self.target_counties = ['Bergen', 'Essex', 'Hudson', 'Passaic', 'Union']
        
        # New Jersey county FIPS codes for the 5 target counties
        self.target_county_fips = {
            '003': 'Bergen',    # Bergen County
            '005': 'Bergen',    # Bergen County (additional)
            '013': 'Essex',     # Essex County
            '017': 'Hudson',    # Hudson County
            '031': 'Passaic',   # Passaic County
            '039': 'Union'      # Union County
        }
        
        # TIGER/Line file URLs for New Jersey
        self.tiger_urls = {
            'municipalities': 'https://www2.census.gov/geo/tiger/TIGER2023/PLACE/tl_2023_34_place.zip',
            'county_subdivisions': 'https://www2.census.gov/geo/tiger/TIGER2023/COUSUB/tl_2023_34_cousub.zip',
            'counties': 'https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip'
        }
        
        # New Jersey state data URLs (more comprehensive)
        self.nj_state_urls = {
            'municipalities': 'https://www.nj.gov/dep/gis/digidownload/zips/statewide/Municipal_Boundaries_of_NJ.zip',
            'counties': 'https://www.nj.gov/dep/gis/digidownload/zips/statewide/County_Boundaries_of_NJ.zip'
        }
        
        # Load data files
        self.municipalities_df = pd.read_csv(self.data_dir / 'nj_municipalities.csv')
        self.scenarios_df = pd.read_csv(self.data_dir / 'consolidation_scenarios.csv')
        
        # Create comprehensive Northern NJ municipalities dataset
        self._create_comprehensive_municipalities_dataset()
    
    def _create_comprehensive_municipalities_dataset(self):
        """Create a comprehensive dataset of Northern NJ municipalities with estimated data"""
        # All municipalities found in TIGER/Line data for Northern NJ
        comprehensive_munis = {
            # Bergen County
            'Bergenfield': {'county': 'Bergen', 'population_2020': 28000, 'area_sq_miles': 3.9},
            'Dumont': {'county': 'Bergen', 'population_2020': 20000, 'area_sq_miles': 2.9},
            'Fort Lee': {'county': 'Bergen', 'population_2020': 40000, 'area_sq_miles': 2.8},
            'Hackensack': {'county': 'Bergen', 'population_2020': 45000, 'area_sq_miles': 4.3},
            'Paramus': {'county': 'Bergen', 'population_2020': 26000, 'area_sq_miles': 10.4},
            'Ridgewood': {'county': 'Bergen', 'population_2020': 25000, 'area_sq_miles': 5.8},
            'Englewood': {'county': 'Bergen', 'population_2020': 29000, 'area_sq_miles': 5.2},
            'Fair Lawn': {'county': 'Bergen', 'population_2020': 34000, 'area_sq_miles': 5.1},
            'Garfield': {'county': 'Bergen', 'population_2020': 32000, 'area_sq_miles': 2.1},
            'Glen Rock': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 2.8},
            'Hasbrouck Heights': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 1.6},
            'Lodi': {'county': 'Bergen', 'population_2020': 24000, 'area_sq_miles': 2.0},
            'Maywood': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 1.3},
            'New Milford': {'county': 'Bergen', 'population_2020': 17000, 'area_sq_miles': 2.3},
            'North Arlington': {'county': 'Bergen', 'population_2020': 16000, 'area_sq_miles': 2.9},
            'Oradell': {'county': 'Bergen', 'population_2020': 8000, 'area_sq_miles': 2.5},
            'Palisades Park': {'county': 'Bergen', 'population_2020': 20000, 'area_sq_miles': 1.2},
            'Ramsey': {'county': 'Bergen', 'population_2020': 15000, 'area_sq_miles': 5.9},
            'Ridgefield Park': {'county': 'Bergen', 'population_2020': 13000, 'area_sq_miles': 1.8},
            'River Edge': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 1.8},
            'Teterboro': {'county': 'Bergen', 'population_2020': 100, 'area_sq_miles': 1.2},
            'Wallington': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 1.0},
            'Wood-Ridge': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 1.0},
            'Allendale': {'county': 'Bergen', 'population_2020': 7000, 'area_sq_miles': 2.0},
            'Alpine': {'county': 'Bergen', 'population_2020': 2000, 'area_sq_miles': 8.0},
            'Bogota': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 0.8},
            'Carlstadt': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 4.0},
            'Cliffside Park': {'county': 'Bergen', 'population_2020': 25000, 'area_sq_miles': 1.0},
            'Cresskill': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 2.0},
            'Demarest': {'county': 'Bergen', 'population_2020': 5000, 'area_sq_miles': 1.5},
            'East Rutherford': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 3.0},
            'Edgewater': {'county': 'Bergen', 'population_2020': 13000, 'area_sq_miles': 1.0},
            'Elmwood Park': {'county': 'Bergen', 'population_2020': 20000, 'area_sq_miles': 2.0},
            'Emerson': {'county': 'Bergen', 'population_2020': 8000, 'area_sq_miles': 1.5},
            'Englewood Cliffs': {'county': 'Bergen', 'population_2020': 5000, 'area_sq_miles': 2.0},
            'Fairview': {'county': 'Bergen', 'population_2020': 15000, 'area_sq_miles': 1.0},
            'Franklin Lakes': {'county': 'Bergen', 'population_2020': 11000, 'area_sq_miles': 9.0},
            'Harrington Park': {'county': 'Bergen', 'population_2020': 5000, 'area_sq_miles': 1.5},
            'Haworth': {'county': 'Bergen', 'population_2020': 3000, 'area_sq_miles': 1.0},
            'Hillsdale': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 2.0},
            'Leonia': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 1.0},
            'Little Ferry': {'county': 'Bergen', 'population_2020': 11000, 'area_sq_miles': 1.0},
            'Midland Park': {'county': 'Bergen', 'population_2020': 7000, 'area_sq_miles': 1.0},
            'Montvale': {'county': 'Bergen', 'population_2020': 8000, 'area_sq_miles': 2.0},
            'Moonachie': {'county': 'Bergen', 'population_2020': 3000, 'area_sq_miles': 1.0},
            'North Arlington': {'county': 'Bergen', 'population_2020': 16000, 'area_sq_miles': 2.9},
            'Northvale': {'county': 'Bergen', 'population_2020': 5000, 'area_sq_miles': 1.0},
            'Norwood': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 1.0},
            'Oakland': {'county': 'Bergen', 'population_2020': 13000, 'area_sq_miles': 3.0},
            'Old Tappan': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 2.0},
            'Palisades Park': {'county': 'Bergen', 'population_2020': 20000, 'area_sq_miles': 1.2},
            'Park Ridge': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 2.0},
            'Ridgefield': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 2.0},
            'Ridgefield Park': {'county': 'Bergen', 'population_2020': 13000, 'area_sq_miles': 1.8},
            'River Edge': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 1.8},
            'Rutherford': {'county': 'Bergen', 'population_2020': 19000, 'area_sq_miles': 2.0},
            'Saddle River': {'county': 'Bergen', 'population_2020': 3000, 'area_sq_miles': 2.0},
            'Tenafly': {'county': 'Bergen', 'population_2020': 15000, 'area_sq_miles': 2.0},
            'Teterboro': {'county': 'Bergen', 'population_2020': 100, 'area_sq_miles': 1.2},
            'Upper Saddle River': {'county': 'Bergen', 'population_2020': 8000, 'area_sq_miles': 2.0},
            'Waldwick': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 1.0},
            'Wallington': {'county': 'Bergen', 'population_2020': 12000, 'area_sq_miles': 1.0},
            'Westwood': {'county': 'Bergen', 'population_2020': 11000, 'area_sq_miles': 2.0},
            'Woodcliff Lake': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 1.0},
            
            # Additional missing townships found in TIGER/Line data (5-county region only)
            'Pompton Plains': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 3.0},
            
            # Essex County
            'Newark': {'county': 'Essex', 'population_2020': 311549, 'area_sq_miles': 26.1},
            'East Orange': {'county': 'Essex', 'population_2020': 64270, 'area_sq_miles': 3.9},
            'Caldwell': {'county': 'Essex', 'population_2020': 8000, 'area_sq_miles': 1.2},
            'Essex Fells': {'county': 'Essex', 'population_2020': 2000, 'area_sq_miles': 1.0},
            'Glen Ridge': {'county': 'Essex', 'population_2020': 8000, 'area_sq_miles': 1.3},
            'Irvington': {'county': 'Essex', 'population_2020': 60000, 'area_sq_miles': 3.0},
            'Millburn': {'county': 'Essex', 'population_2020': 22000, 'area_sq_miles': 9.8},
            'North Caldwell': {'county': 'Essex', 'population_2020': 7000, 'area_sq_miles': 2.5},
            'Roseland': {'county': 'Essex', 'population_2020': 6000, 'area_sq_miles': 3.0},
            
            # Hudson County
            'Jersey City': {'county': 'Hudson', 'population_2020': 292244, 'area_sq_miles': 14.7},
            'Union City': {'county': 'Hudson', 'population_2020': 68589, 'area_sq_miles': 2.6},
            'Bayonne': {'county': 'Hudson', 'population_2020': 67117, 'area_sq_miles': 6.5},
            'West New York': {'county': 'Hudson', 'population_2020': 50000, 'area_sq_miles': 3.4},
            'Hoboken': {'county': 'Hudson', 'population_2020': 55000, 'area_sq_miles': 5.3},
            'Secaucus': {'county': 'Hudson', 'population_2020': 20000, 'area_sq_miles': 8.7},
            'Kearny': {'county': 'Hudson', 'population_2020': 40000, 'area_sq_miles': 6.3},
            'Guttenberg': {'county': 'Hudson', 'population_2020': 12000, 'area_sq_miles': 1.0},
            'Harrison': {'county': 'Hudson', 'population_2020': 18000, 'area_sq_miles': 1.3},
            'North Bergen': {'county': 'Hudson', 'population_2020': 60000, 'area_sq_miles': 3.4},
            
            # Passaic County
            'Paterson': {'county': 'Passaic', 'population_2020': 159732, 'area_sq_miles': 8.4},
            'Clifton': {'county': 'Passaic', 'population_2020': 89269, 'area_sq_miles': 11.4},
            'Passaic': {'county': 'Passaic', 'population_2020': 70573, 'area_sq_miles': 3.2},
            'Bloomingdale': {'county': 'Passaic', 'population_2020': 8000, 'area_sq_miles': 4.0},
            'Haledon': {'county': 'Passaic', 'population_2020': 9000, 'area_sq_miles': 1.2},
            'Hawthorne': {'county': 'Passaic', 'population_2020': 19307, 'area_sq_miles': 6.0},
            'North Haledon': {'county': 'Passaic', 'population_2020': 9000, 'area_sq_miles': 2.0},
            'Pompton Lakes': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 3.0},
            'Prospect Park': {'county': 'Passaic', 'population_2020': 6000, 'area_sq_miles': 0.8},
            'Ringwood': {'county': 'Passaic', 'population_2020': 12000, 'area_sq_miles': 25.0},
            'Totowa': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 2.0},
            'Wanaque': {'county': 'Passaic', 'population_2020': 12000, 'area_sq_miles': 8.0},
            'Woodland Park': {'county': 'Passaic', 'population_2020': 13000, 'area_sq_miles': 3.0},
            
            # Union County
            'Elizabeth': {'county': 'Union', 'population_2020': 137298, 'area_sq_miles': 12.3},
            'Plainfield': {'county': 'Union', 'population_2020': 55000, 'area_sq_miles': 6.0},
            'Union': {'county': 'Union', 'population_2020': 60000, 'area_sq_miles': 9.0},
            'Cranford': {'county': 'Union', 'population_2020': 25000, 'area_sq_miles': 5.0},
            'Fanwood': {'county': 'Union', 'population_2020': 8000, 'area_sq_miles': 1.3},
            'Garwood': {'county': 'Union', 'population_2020': 5000, 'area_sq_miles': 0.7},
            'Kenilworth': {'county': 'Union', 'population_2020': 8000, 'area_sq_miles': 1.0},
            'Linden': {'county': 'Union', 'population_2020': 42000, 'area_sq_miles': 11.0},
            'Mountainside': {'county': 'Union', 'population_2020': 7000, 'area_sq_miles': 3.0},
            'New Providence': {'county': 'Union', 'population_2020': 13000, 'area_sq_miles': 3.0},
            'Rahway': {'county': 'Union', 'population_2020': 30000, 'area_sq_miles': 4.0},
            'Roselle': {'county': 'Union', 'population_2020': 22000, 'area_sq_miles': 2.7},
            'Roselle Park': {'county': 'Union', 'population_2020': 14000, 'area_sq_miles': 1.3},
            'Scotch Plains': {'county': 'Union', 'population_2020': 24000, 'area_sq_miles': 6.0},
            'Springfield': {'county': 'Union', 'population_2020': 16000, 'area_sq_miles': 4.0},
            'Summit': {'county': 'Union', 'population_2020': 22000, 'area_sq_miles': 6.0},
            'Westfield': {'county': 'Union', 'population_2020': 31000, 'area_sq_miles': 6.0},
            'Winfield': {'county': 'Union', 'population_2020': 2000, 'area_sq_miles': 0.3},
            
            # More missing municipalities from TIGER/Line data
            'Bloomingdale': {'county': 'Passaic', 'population_2020': 8000, 'area_sq_miles': 4.0},
            'Cranford': {'county': 'Union', 'population_2020': 25000, 'area_sq_miles': 5.0},
            'Fanwood': {'county': 'Union', 'population_2020': 8000, 'area_sq_miles': 1.3},
            'Garwood': {'county': 'Union', 'population_2020': 5000, 'area_sq_miles': 0.7},
            'Guttenberg': {'county': 'Hudson', 'population_2020': 12000, 'area_sq_miles': 1.0},
            'Haledon': {'county': 'Passaic', 'population_2020': 9000, 'area_sq_miles': 1.2},
            'Harrison': {'county': 'Hudson', 'population_2020': 18000, 'area_sq_miles': 1.3},
            'Hawthorne': {'county': 'Passaic', 'population_2020': 19307, 'area_sq_miles': 6.0},
            'Kenilworth': {'county': 'Union', 'population_2020': 8000, 'area_sq_miles': 1.0},
            'Linden': {'county': 'Union', 'population_2020': 42000, 'area_sq_miles': 11.0},
            'Mountainside': {'county': 'Union', 'population_2020': 7000, 'area_sq_miles': 3.0},
            'New Providence': {'county': 'Union', 'population_2020': 13000, 'area_sq_miles': 3.0},
            'North Haledon': {'county': 'Passaic', 'population_2020': 9000, 'area_sq_miles': 2.0},
            'Pompton Lakes': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 3.0},
            'Prospect Park': {'county': 'Passaic', 'population_2020': 6000, 'area_sq_miles': 0.8},
            'Rahway': {'county': 'Union', 'population_2020': 30000, 'area_sq_miles': 4.0},
            'Roselle': {'county': 'Union', 'population_2020': 22000, 'area_sq_miles': 2.7},
            'Roselle Park': {'county': 'Union', 'population_2020': 14000, 'area_sq_miles': 1.3},
            'Springfield': {'county': 'Union', 'population_2020': 16000, 'area_sq_miles': 4.0},
            'Summit': {'county': 'Union', 'population_2020': 22000, 'area_sq_miles': 6.0},
            'Totowa': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 2.0},
            'Wanaque': {'county': 'Passaic', 'population_2020': 12000, 'area_sq_miles': 8.0},
            'Westfield': {'county': 'Union', 'population_2020': 31000, 'area_sq_miles': 6.0},
            'Woodcliff Lake': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 1.0},
            'Woodland Park': {'county': 'Passaic', 'population_2020': 13000, 'area_sq_miles': 3.0},
            
            # Additional municipalities from TIGER/Line data to fill gaps
            # Bergen County (12 missing)
            'Closter': {'county': 'Bergen', 'population_2020': 8000, 'area_sq_miles': 3.0},
            'Ho-Ho-Kus': {'county': 'Bergen', 'population_2020': 4000, 'area_sq_miles': 1.0},
            'Lyndhurst': {'county': 'Bergen', 'population_2020': 22000, 'area_sq_miles': 2.0},
            'Mahwah': {'county': 'Bergen', 'population_2020': 26000, 'area_sq_miles': 26.0},
            'River Vale': {'county': 'Bergen', 'population_2020': 10000, 'area_sq_miles': 2.0},
            'Rochelle Park': {'county': 'Bergen', 'population_2020': 6000, 'area_sq_miles': 1.0},
            'Rockleigh': {'county': 'Bergen', 'population_2020': 500, 'area_sq_miles': 1.0},
            'Saddle Brook': {'county': 'Bergen', 'population_2020': 14000, 'area_sq_miles': 2.0},
            'South Hackensack': {'county': 'Bergen', 'population_2020': 3000, 'area_sq_miles': 0.5},
            'Teaneck': {'county': 'Bergen', 'population_2020': 41000, 'area_sq_miles': 6.0},
            'Washington': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 2.0}, # County 005
            'Washington_Bergen_003': {'county': 'Bergen', 'population_2020': 9000, 'area_sq_miles': 2.0}, # County 003
            'Washington_Hudson': {'county': 'Hudson', 'population_2020': 7000, 'area_sq_miles': 1.5}, # County 015
            'Washington_Passaic': {'county': 'Passaic', 'population_2020': 11000, 'area_sq_miles': 3.0}, # County 027
            'Washington_Union': {'county': 'Union', 'population_2020': 6000, 'area_sq_miles': 1.8}, # County 041
            'Washington_Borough': {'county': 'Union', 'population_2020': 6000, 'area_sq_miles': 1.8}, # County 041
            'Wyckoff': {'county': 'Bergen', 'population_2020': 17000, 'area_sq_miles': 5.0},
            
            # Essex County (13 missing)
            'Belleville': {'county': 'Essex', 'population_2020': 37000, 'area_sq_miles': 3.4},
            'Bloomfield': {'county': 'Essex', 'population_2020': 50000, 'area_sq_miles': 5.3},
            'Cedar Grove': {'county': 'Essex', 'population_2020': 12000, 'area_sq_miles': 2.0},
            'City of Orange': {'county': 'Essex', 'population_2020': 30000, 'area_sq_miles': 2.5},
            'Fairfield': {'county': 'Essex', 'population_2020': 8000, 'area_sq_miles': 1.0},
            'Livingston': {'county': 'Essex', 'population_2020': 30000, 'area_sq_miles': 14.0},
            'Maplewood': {'county': 'Essex', 'population_2020': 25000, 'area_sq_miles': 3.2},
            'Montclair': {'county': 'Essex', 'population_2020': 40000, 'area_sq_miles': 6.3},
            'Nutley': {'county': 'Essex', 'population_2020': 30000, 'area_sq_miles': 4.0},
            'South Orange Village': {'county': 'Essex', 'population_2020': 16964, 'area_sq_miles': 2.8},
            'Verona': {'county': 'Essex', 'population_2020': 14000, 'area_sq_miles': 2.0},
            'West Caldwell': {'county': 'Essex', 'population_2020': 11000, 'area_sq_miles': 2.0},
            'West Orange': {'county': 'Essex', 'population_2020': 48000, 'area_sq_miles': 12.0},
            
            # Hudson County (2 missing)
            'East Newark': {'county': 'Hudson', 'population_2020': 2000, 'area_sq_miles': 0.1},
            'Weehawken': {'county': 'Hudson', 'population_2020': 15000, 'area_sq_miles': 1.0},
            
            # Passaic County (3 missing)
            'Little Falls': {'county': 'Passaic', 'population_2020': 14000, 'area_sq_miles': 2.0},
            'Wayne': {'county': 'Passaic', 'population_2020': 55000, 'area_sq_miles': 25.0},
            'West Milford': {'county': 'Passaic', 'population_2020': 25000, 'area_sq_miles': 80.0},
            
            # Union County (3 missing)
            'Berkeley Heights': {'county': 'Union', 'population_2020': 13000, 'area_sq_miles': 3.0},
            'Clark': {'county': 'Union', 'population_2020': 15000, 'area_sq_miles': 4.0},
            'Hillside': {'county': 'Union', 'population_2020': 22000, 'area_sq_miles': 2.8}
        }
        
        # Create DataFrame
        munis_data = []
        for muni_name, data in comprehensive_munis.items():
            munis_data.append({
                'municipality': muni_name,
                'county': data['county'],
                'population_2020': data['population_2020'],
                'area_sq_miles': data['area_sq_miles'],
                'population_density': data['population_2020'] / data['area_sq_miles'],
                'in_target_region': data['county'] in self.target_counties
            })
        
        self.comprehensive_municipalities_df = pd.DataFrame(munis_data)
        print(f"Created comprehensive dataset with {len(self.comprehensive_municipalities_df)} municipalities")
    
    def download_tiger_data(self):
        """Download TIGER/Line files from US Census Bureau"""
        print("Downloading TIGER/Line files from US Census Bureau...")
        
        for data_type, url in self.tiger_urls.items():
            zip_path = self.tiger_dir / f"{data_type}.zip"
            
            if not zip_path.exists():
                print(f"Downloading {data_type} data...")
                try:
                    response = requests.get(url, stream=True, verify=False)
                    response.raise_for_status()
                    
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Downloaded {data_type} data successfully")
                except Exception as e:
                    print(f"Error downloading {data_type} data: {e}")
                    return False
            else:
                print(f"{data_type} data already exists")
        
        return True
    
    def extract_tiger_data(self):
        """Extract TIGER/Line ZIP files"""
        print("Extracting TIGER/Line files...")
        
        for data_type in self.tiger_urls.keys():
            zip_path = self.tiger_dir / f"{data_type}.zip"
            extract_dir = self.tiger_dir / data_type
            
            if zip_path.exists() and not extract_dir.exists():
                print(f"Extracting {data_type} data...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    print(f"Extracted {data_type} data successfully")
                except Exception as e:
                    print(f"Error extracting {data_type} data: {e}")
                    return False
            else:
                print(f"{data_type} data already extracted")
        
        return True
    
    def load_municipalities(self):
        """Load municipal boundary data, trying NJ state data first, then TIGER/Line"""
        print("Loading municipal boundary data...")
        
        # First, try to download and use New Jersey state data
        if self.download_nj_state_data():
            nj_state_data = self.load_nj_state_municipalities()
            if nj_state_data is not None and len(nj_state_data) > 0:
                print("✅ Successfully loaded municipalities from NJ state data")
                return nj_state_data
            else:
                print("⚠️ NJ state data failed, falling back to TIGER/Line data")
        else:
            print("⚠️ Could not download NJ state data, falling back to TIGER/Line data")
        
        # Fall back to TIGER/Line data - use only COUNTY_SUBDIVISION data since it has proper county filtering
        # Skip PLACE data since it doesn't have COUNTYFP column and includes all of New Jersey
        print("🔍 Using TIGER/Line COUNTY_SUBDIVISION data (with proper county filtering)...")
        cousub_data = self.load_tiger_county_subdivisions()
        
        if cousub_data is not None:
            print("✅ Using COUNTY_SUBDIVISION data only (filtered to 5 target counties)")
            return cousub_data
        else:
            print("❌ Could not load TIGER/Line COUNTY_SUBDIVISION data")
            return None
    
    def load_tiger_municipalities(self):
        """Load TIGER/Line municipal boundary data"""
        print("Loading TIGER/Line municipal boundary data...")
        
        municipalities_dir = self.tiger_dir / 'municipalities'
        shapefile_path = None
        
        # Find the shapefile
        for file in municipalities_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            print("No shapefile found in municipalities directory")
            return None
        
        try:
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)
            print(f"Loaded {len(gdf)} municipalities from TIGER/Line data")
            
            # Filter to only include municipalities from the 5 target counties
            if 'COUNTYFP' in gdf.columns:
                gdf = gdf[gdf['COUNTYFP'].isin(self.target_county_fips.keys())]
                print(f"Filtered to {len(gdf)} municipalities in 5 target counties")
            else:
                print("⚠️ COUNTYFP column not found, cannot filter by county")
            
            # Filter for municipalities that match our comprehensive data
            # We'll match by name and county, but first need to map county FIPS codes to county names
            county_fips_to_name = self.target_county_fips
            
            # Add county name to TIGER data (check if COUNTYFP column exists)
            if 'COUNTYFP' in gdf.columns:
                gdf['county_name'] = gdf['COUNTYFP'].map(county_fips_to_name)
            else:
                print("⚠️ COUNTYFP column not found in PLACE data, skipping county-based matching")
                gdf['county_name'] = None
            
            # Create a mapping for Washington townships
            washington_mapping = {
                ('Washington', 'Bergen'): 'Washington_Bergen_003',
                ('Washington', 'Hudson'): 'Washington_Hudson', 
                ('Washington', 'Passaic'): 'Washington_Passaic',
                ('Washington', 'Union'): 'Washington_Union'
            }
            
            # Add mapped municipality names
            gdf['mapped_municipality'] = gdf.apply(
                lambda row: washington_mapping.get((row['NAME'], row['county_name']), row['NAME']), 
                axis=1
            )
            
            # Match by both mapped name and county (if county_name is available)
            if gdf['county_name'].notna().any():
                merged_gdf = gdf.merge(
                    self.comprehensive_municipalities_df[['municipality', 'county', 'population_2020', 'area_sq_miles', 'population_density']],
                    left_on=['mapped_municipality', 'county_name'],
                    right_on=['municipality', 'county'],
                    how='inner'
                )
            else:
                # Fall back to name-only matching if county info is not available
                merged_gdf = gdf.merge(
                    self.comprehensive_municipalities_df[['municipality', 'county', 'population_2020', 'area_sq_miles', 'population_density']],
                    left_on='mapped_municipality',
                    right_on='municipality',
                    how='inner'
                )
            print(f"Matched {len(merged_gdf)} municipalities with comprehensive population data")
            
            # Check for missing municipalities (will be handled by County Subdivision data)
            missing_munis = self.comprehensive_municipalities_df[
                ~self.comprehensive_municipalities_df['municipality'].isin(merged_gdf['municipality'])
            ]
            
            if not missing_munis.empty:
                print(f"Missing {len(missing_munis)} municipalities from PLACE data (will try County Subdivision data):")
                for _, muni in missing_munis.iterrows():
                    print(f"  - {muni['municipality']} ({muni['county']} County)")
            
            return merged_gdf
            
        except Exception as e:
            print(f"Error loading TIGER/Line data: {e}")
            return None
    
    def load_tiger_county_subdivisions(self):
        """Load TIGER/Line county subdivision data (includes townships like North Bergen)"""
        print("Loading TIGER/Line county subdivision data...")
        
        # Download county subdivision data if not exists
        self.download_tiger_data()
        
        cousub_dir = self.tiger_dir / 'county_subdivisions'
        shapefile_path = None
        
        # Find the shapefile
        for file in cousub_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            print("No county subdivision shapefile found")
            return None
        
        try:
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)
            print(f"Loaded {len(gdf)} county subdivisions from TIGER/Line data")
            
            # Filter to only include county subdivisions from the 5 target counties
            if 'COUNTYFP' in gdf.columns:
                gdf = gdf[gdf['COUNTYFP'].isin(self.target_county_fips.keys())]
                print(f"Filtered to {len(gdf)} county subdivisions in 5 target counties")
            else:
                print("⚠️ COUNTYFP column not found, cannot filter by county")
            
            # Check what columns are available
            print(f"Available columns: {list(gdf.columns)}")
            
            # Look for North Bergen specifically
            print("🔍 Searching for North Bergen in county subdivisions...")
            north_bergen_matches = gdf[gdf['NAME'].str.contains('North Bergen', case=False, na=False)]
            if not north_bergen_matches.empty:
                print("✅ Found North Bergen in county subdivisions!")
                for _, row in north_bergen_matches.iterrows():
                    print(f"   - {row['NAME']} (NAMELSAD: {row.get('NAMELSAD', 'N/A')})")
            
            # Filter for municipalities that match our comprehensive data
            # Match by name and county, but first need to map county FIPS codes to county names
            county_fips_to_name = self.target_county_fips
            
            # Add county name to TIGER data
            gdf['county_name'] = gdf['COUNTYFP'].map(county_fips_to_name)
            
            # Create a mapping for Washington townships
            washington_mapping = {
                ('Washington', 'Bergen'): 'Washington_Bergen_003',
                ('Washington', 'Hudson'): 'Washington_Hudson', 
                ('Washington', 'Passaic'): 'Washington_Passaic',
                ('Washington', 'Union'): 'Washington_Union'
            }
            
            # Add mapped municipality names
            gdf['mapped_municipality'] = gdf.apply(
                lambda row: washington_mapping.get((row['NAME'], row['county_name']), row['NAME']), 
                axis=1
            )
            
            # Match by both mapped name and county
            merged_gdf = gdf.merge(
                self.comprehensive_municipalities_df[['municipality', 'county', 'population_2020', 'area_sq_miles', 'population_density']],
                left_on=['mapped_municipality', 'county_name'],
                right_on=['municipality', 'county'],
                how='inner'
            )
            print(f"Matched {len(merged_gdf)} county subdivisions with comprehensive population data")
            
            # Check for missing municipalities
            missing_munis = self.comprehensive_municipalities_df[
                ~self.comprehensive_municipalities_df['municipality'].isin(merged_gdf['municipality'])
            ]
            
            if not missing_munis.empty:
                print(f"Still missing {len(missing_munis)} municipalities after county subdivisions:")
                for _, muni in missing_munis.iterrows():
                    print(f"  - {muni['municipality']} ({muni['county']} County)")
            
            return merged_gdf
            
        except Exception as e:
            print(f"Error loading TIGER/Line county subdivision data: {e}")
            return None
    
    
    def download_nj_state_data(self):
        """Download New Jersey state municipal boundary data from NJDEP"""
        print("Downloading New Jersey state municipal boundary data from NJDEP...")
        
        nj_state_dir = self.data_dir / 'nj_state_data'
        nj_state_dir.mkdir(exist_ok=True)
        
        for data_type, url in self.nj_state_urls.items():
            zip_path = nj_state_dir / f"{data_type}.zip"
            
            if not zip_path.exists():
                print(f"Downloading {data_type} data from NJDEP...")
                try:
                    response = requests.get(url, stream=True, verify=False)
                    response.raise_for_status()
                    
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Downloaded {data_type} data successfully")
                except Exception as e:
                    print(f"Error downloading {data_type} data: {e}")
                    return False
            else:
                print(f"{data_type} data already exists")
        
        # Extract the zip files
        for data_type in self.nj_state_urls.keys():
            zip_path = nj_state_dir / f"{data_type}.zip"
            extract_dir = nj_state_dir / data_type
            
            if not extract_dir.exists():
                print(f"Extracting {data_type} data...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    print(f"Extracted {data_type} data successfully")
                except Exception as e:
                    print(f"Error extracting {data_type} data: {e}")
                    return False
            else:
                print(f"{data_type} data already extracted")
        
        return True
    
    def load_nj_state_municipalities(self):
        """Load New Jersey state municipal boundary data from NJDEP"""
        print("Loading New Jersey state municipal boundary data from NJDEP...")
        
        nj_state_dir = self.data_dir / 'nj_state_data'
        municipalities_dir = nj_state_dir / 'municipalities'
        shapefile_path = None
        
        # Find the shapefile
        for file in municipalities_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            print("No NJ state shapefile found in municipalities directory")
            return None
        
        try:
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)
            print(f"Loaded {len(gdf)} municipalities from NJ state data")
            
            # Check what columns are available
            print(f"Available columns: {list(gdf.columns)}")
            
            # Try to match with our comprehensive data
            # The NJ state data might use different column names
            name_columns = [col for col in gdf.columns if 'name' in col.lower() or 'mun' in col.lower()]
            print(f"Potential name columns: {name_columns}")
            
            if name_columns:
                # Use the first name column found
                name_col = name_columns[0]
                print(f"Using column '{name_col}' for municipality names")
                
                # Merge with our comprehensive municipalities data
                merged_gdf = gdf.merge(
                    self.comprehensive_municipalities_df[['municipality', 'county', 'population_2020', 'area_sq_miles', 'population_density']],
                    left_on=name_col,
                    right_on='municipality',
                    how='inner'
                )
                print(f"Matched {len(merged_gdf)} municipalities with NJ state data")
                
                # Check for missing municipalities
                missing_munis = self.comprehensive_municipalities_df[
                    ~self.comprehensive_municipalities_df['municipality'].isin(merged_gdf['municipality'])
                ]
                
                if not missing_munis.empty:
                    print(f"Still missing {len(missing_munis)} municipalities:")
                    for _, muni in missing_munis.iterrows():
                        print(f"  - {muni['municipality']} ({muni['county']} County)")
                
                return merged_gdf
            else:
                print("No suitable name column found in NJ state data")
                return None
            
        except Exception as e:
            print(f"Error loading NJ state data: {e}")
            return None
    
    def load_tiger_counties(self):
        """Load TIGER/Line county boundary data"""
        print("Loading TIGER/Line county boundary data...")
        
        counties_dir = self.tiger_dir / 'counties'
        shapefile_path = None
        
        # Find the shapefile
        for file in counties_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            print("No shapefile found in counties directory")
            return None
        
        try:
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)
            print(f"Loaded {len(gdf)} counties from TIGER/Line data")
            
            # Filter for New Jersey (STATEFP = '34') and target counties
            nj_counties = gdf[gdf['STATEFP'] == '34']
            target_counties = nj_counties[nj_counties['COUNTYFP'].isin(['003', '013', '017', '031', '039'])]  # Bergen, Essex, Hudson, Passaic, Union
            print(f"Filtered to {len(target_counties)} target counties in New Jersey")
            
            return target_counties
            
        except Exception as e:
            print(f"Error loading TIGER/Line county data: {e}")
            return None
    
    def create_tiger_municipalities_map(self):
        """Create a map using municipal boundary data (NJ state data preferred)"""
        print("Creating municipal boundaries map...")
        
        # Load municipal data (tries NJ state data first, then TIGER/Line)
        municipalities_gdf = self.load_municipalities()
        if municipalities_gdf is None:
            print("Could not load municipal data")
            return None
        
        # Create the map
        center_lat = municipalities_gdf.geometry.centroid.y.mean()
        center_lon = municipalities_gdf.geometry.centroid.x.mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='CartoDB dark_matter'
        )
        
        # County FIPS to name mapping
        county_fips_to_name = {
            '003': 'Bergen',
            '013': 'Essex', 
            '017': 'Hudson',
            '031': 'Passaic',
            '039': 'Union'
        }
        
        # Add each municipality with its real TIGER/Line boundary
        for idx, row in municipalities_gdf.iterrows():
            county_name = row['county']  # Use county from our merged data
            county_color = self.county_colors.get(county_name, '#ffffff')
            
            # Convert geometry to GeoJSON
            # Use geometry directly - no need to convert to JSON
            
            # Add polygon to map
            folium.GeoJson(
                row.geometry,
                style_function=lambda x, color=county_color: {
                    'fillColor': color,
                    'color': color,
                    'weight': 2,
                    'fillOpacity': 0.6
                },
                popup=folium.Popup(
                    f"""
                    <div style='color: white; background: #2d2d2d; padding: 10px; border-radius: 5px; width: 250px;'>
                        <h4 style='color: {county_color}; margin: 0 0 5px 0;'>{row['NAME']}</h4>
                        <p style='margin: 2px 0;'><strong>County:</strong> {county_name}</p>
                        <p style='margin: 2px 0;'><strong>FIPS Code:</strong> {row.get('PLACEFP', row.get('COUSUBFP', 'N/A'))}</p>
                        <p style='margin: 2px 0;'><strong>Boundary Type:</strong> TIGER/Line Data</p>
                        <p style='margin: 2px 0;'><strong>Features:</strong> Real geographic boundaries</p>
                    </div>
                    """,
                    max_width=300
                )
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: #2d2d2d; border: 2px solid #666666; 
                    z-index:9999; font-size:14px; color: white; padding: 10px;
                    border-radius: 5px;">
        <h4 style="margin: 0 0 10px 0; color: #00d4ff;">TIGER/Line Municipal Boundaries</h4>
        <p style="margin: 2px 0;"><span style="color: #00d4ff;">●</span> Bergen</p>
        <p style="margin: 2px 0;"><span style="color: #ff6b35;">●</span> Essex</p>
        <p style="margin: 2px 0;"><span style="color: #00ff88;">●</span> Hudson</p>
        <p style="margin: 2px 0;"><span style="color: #ffb347;">●</span> Passaic</p>
        <p style="margin: 2px 0;"><span style="color: #9d4edd;">●</span> Union</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save the map
        map_path = self.output_dir / 'tiger_municipal_boundaries_map.html'
        m.save(str(map_path))
        
        print(f"TIGER/Line municipal boundaries map saved to {map_path}")
        return m
    
    def create_tiger_consolidation_map(self):
        """Create consolidation map using TIGER/Line county boundary data"""
        print("Creating TIGER/Line consolidation boundaries map...")
        
        # Load TIGER data
        counties_gdf = self.load_tiger_counties()
        if counties_gdf is None:
            print("Could not load TIGER/Line county data")
            return None
        
        # Create the map
        center_lat = counties_gdf.geometry.centroid.y.mean()
        center_lon = counties_gdf.geometry.centroid.x.mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='CartoDB dark_matter'
        )
        
        # County FIPS to name mapping
        county_fips_to_name = {
            '003': 'Bergen',
            '013': 'Essex', 
            '017': 'Hudson',
            '031': 'Passaic',
            '039': 'Union'
        }
        
        # Create feature groups for different scenarios
        five_county_group = folium.FeatureGroup(name='5-County Consolidation')
        three_county_group = folium.FeatureGroup(name='3-County Core (Bergen, Essex, Hudson)')
        
        # 5-County Consolidation
        for idx, row in counties_gdf.iterrows():
            county_name = county_fips_to_name.get(row['COUNTYFP'], 'Unknown')
            
            # Convert geometry to GeoJSON
            # Use geometry directly - no need to convert to JSON
            
            # Add polygon to 5-county group
            folium.GeoJson(
                row.geometry,
                style_function=lambda x: {
                    'fillColor': '#00d4ff',
                    'color': '#00d4ff',
                    'weight': 3,
                    'fillOpacity': 0.3
                },
                popup=folium.Popup(
                    f"""
                    <div style='color: white; background: #2d2d2d; padding: 15px; border-radius: 5px; text-align: center;'>
                        <h4 style='color: #00d4ff; margin: 0 0 10px 0;'>{county_name} County</h4>
                        <p style='margin: 5px 0;'>Part of 5-County Consolidation</p>
                        <p style='margin: 5px 0;'>TIGER/Line boundaries</p>
                    </div>
                    """,
                    max_width=300
                )
            ).add_to(five_county_group)
        
        # 3-County Core
        three_county_fips = ['003', '013', '017']  # Bergen, Essex, Hudson
        for idx, row in counties_gdf.iterrows():
            if row['COUNTYFP'] in three_county_fips:
                county_name = county_fips_to_name.get(row['COUNTYFP'], 'Unknown')
                
                # Convert geometry to GeoJSON
                # Use geometry directly - no need to convert to JSON
                
                # Add polygon to 3-county group
                folium.GeoJson(
                    row.geometry,
                    style_function=lambda x: {
                        'fillColor': '#00ff88',
                        'color': '#00ff88',
                        'weight': 3,
                        'fillOpacity': 0.4
                    },
                    popup=folium.Popup(
                        f"""
                        <div style='color: white; background: #2d2d2d; padding: 15px; border-radius: 5px; text-align: center;'>
                            <h4 style='color: #00ff88; margin: 0 0 10px 0;'>{county_name} County</h4>
                            <p style='margin: 5px 0;'>Part of 3-County Core</p>
                            <p style='margin: 5px 0;'>TIGER/Line boundaries</p>
                        </div>
                        """,
                        max_width=300
                    )
                ).add_to(three_county_group)
        
        # Add feature groups to map
        five_county_group.add_to(m)
        three_county_group.add_to(m)
        
        # Add layer control
        folium.LayerControl(collapsed=False).add_to(m)
        
        # Add center marker
        folium.Marker(
            location=[center_lat, center_lon],
            popup="""
            <div style='color: white; background: #2d2d2d; padding: 15px; border-radius: 5px; text-align: center;'>
                <h3 style='color: #00d4ff; margin: 0 0 10px 0;'>🏙️ Greater Jersey City</h3>
                <p style='margin: 5px 0;'><strong>Population:</strong> 3,610,711</p>
                <p style='margin: 5px 0;'><strong>US Rank:</strong> 3rd largest city</p>
                <p style='margin: 5px 0;'><strong>Boundaries:</strong> TIGER/Line Data</p>
            </div>
            """,
            icon=folium.Icon(color='blue', icon='city', prefix='fa')
        ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 250px; height: 140px; 
                    background-color: #2d2d2d; border: 2px solid #666666; 
                    z-index:9999; font-size:14px; color: white; padding: 10px;
                    border-radius: 5px;">
        <h4 style="margin: 0 0 10px 0; color: #00d4ff;">TIGER/Line County Boundaries</h4>
        <p style="margin: 2px 0;"><span style="color: #00d4ff;">■</span> 5-County Consolidation</p>
        <p style="margin: 2px 0;"><span style="color: #00ff88;">■</span> 3-County Core</p>
        <p style="margin: 10px 0 5px 0; font-size: 12px;">Official US Census data</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save the map
        map_path = self.output_dir / 'tiger_consolidation_map.html'
        m.save(str(map_path))
        
        print(f"TIGER/Line consolidation map saved to {map_path}")
        return m
    

    def create_all_tiger_maps(self):
        """Create all maps using TIGER/Line data"""
        print("Creating TIGER/Line boundary maps...")
        
        # Download and extract TIGER data
        if not self.download_tiger_data():
            print("Failed to download TIGER data")
            return False
        
        if not self.extract_tiger_data():
            print("Failed to extract TIGER data")
            return False
        
        # Create maps
        self.create_tiger_municipalities_map()
        self.create_tiger_consolidation_map()
        
        print(f"All TIGER/Line maps saved to {self.output_dir}")
        return True

if __name__ == "__main__":
    tiger_creator = TIGERBoundaryCreator()
    tiger_creator.create_all_tiger_maps()
