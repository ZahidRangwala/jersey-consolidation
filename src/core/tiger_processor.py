"""
TIGER/Line data processor for municipal and county boundaries.
Handles the complex logic of matching municipalities with TIGER/Line data.
"""

import logging
import pandas as pd
import geopandas as gpd
from typing import Dict, List, Optional, Tuple
import folium
from pathlib import Path

from config.settings import (
    VISUALIZATIONS_DIR, COUNTY_COLORS, TARGET_COUNTIES, TARGET_COUNTY_FIPS
)
from .data_manager import DataManager

logger = logging.getLogger(__name__)


class TIGERProcessor:
    """Processes TIGER/Line data for municipal boundaries and creates maps."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.output_dir = VISUALIZATIONS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # County colors for visualization
        self.county_colors = COUNTY_COLORS
        
        # Washington township mapping for handling duplicates
        self.washington_mapping = {
            ('Washington', 'Bergen'): 'Washington_Bergen_003',
            ('Washington', 'Hudson'): 'Washington_Hudson',
            ('Washington', 'Passaic'): 'Washington_Passaic',
            ('Washington', 'Union'): 'Washington_Union',
            ('Washington Borough', 'Union'): 'Washington_Borough'
        }
        
        logger.info("TIGERProcessor initialized")
    
    def load_municipalities(self) -> Optional[gpd.GeoDataFrame]:
        """Load municipal boundary data, trying multiple sources."""
        logger.info("Loading municipal boundary data...")
        
        # Try COUNTY_SUBDIVISION data first (has proper county filtering)
        cousub_data = self._load_county_subdivisions()
        if cousub_data is not None and len(cousub_data) > 0:
            logger.info("✅ Successfully loaded municipalities from COUNTY_SUBDIVISION data")
            return cousub_data
        
        logger.warning("Could not load COUNTY_SUBDIVISION data")
        return None
    
    def _load_county_subdivisions(self) -> Optional[gpd.GeoDataFrame]:
        """Load and process COUNTY_SUBDIVISION data."""
        logger.info("🔍 Using TIGER/Line COUNTY_SUBDIVISION data (with proper county filtering)...")
        
        gdf = self.data_manager.load_tiger_county_subdivisions()
        if gdf is None or gdf.empty:
            return None
        
        # Add county name mapping
        gdf['county_name'] = gdf['COUNTYFP'].map(self.data_manager.target_county_fips)
        
        # Create mapped municipality names for Washington townships
        gdf['mapped_municipality'] = gdf.apply(
            lambda row: self.washington_mapping.get((row['NAME'], row['county_name']), row['NAME']),
            axis=1
        )
        
        # Load comprehensive municipalities dataset
        comprehensive_df = self.data_manager.create_comprehensive_municipalities_dataset()
        
        # Merge with comprehensive data
        merged_gdf = gdf.merge(
            comprehensive_df,
            left_on=['mapped_municipality', 'county_name'],
            right_on=['municipality', 'county'],
            how='inner'
        )
        
        logger.info(f"Matched {len(merged_gdf)} county subdivisions with comprehensive population data")
        
        # Check for missing municipalities
        missing_municipalities = set(comprehensive_df['municipality']) - set(merged_gdf['municipality'])
        if missing_municipalities:
            logger.info(f"Still missing {len(missing_municipalities)} municipalities after county subdivisions:")
            for municipality in sorted(missing_municipalities):
                county = comprehensive_df[comprehensive_df['municipality'] == municipality]['county'].iloc[0]
                logger.info(f"  - {municipality} ({county} County)")
        
        return merged_gdf
    
    def create_municipalities_map(self) -> Optional[folium.Map]:
        """Create an interactive map of municipal boundaries."""
        logger.info("Creating municipal boundaries map...")
        
        municipalities_gdf = self.load_municipalities()
        if municipalities_gdf is None or municipalities_gdf.empty:
            logger.error("No municipal data available for map creation")
            return None
        
        # Calculate map center
        center_lat = municipalities_gdf.geometry.centroid.y.mean()
        center_lon = municipalities_gdf.geometry.centroid.x.mean()
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=9,
            tiles='CartoDB dark_matter'
        )
        
        # Add municipalities
        for _, row in municipalities_gdf.iterrows():
            county_name = row['county']
            county_color = self.county_colors.get(county_name, '#666666')
            
            # Create popup content
            fips_code = row.get('PLACEFP', row.get('COUSUBFP', 'N/A'))
            popup_content = f"""
            <div style='color: white; background: #2d2d2d; padding: 10px; border-radius: 5px; width: 250px;'>
                <h4 style='color: {county_color}; margin: 0 0 5px 0;'>{row['NAME']}</h4>
                <p style='margin: 2px 0;'><strong>County:</strong> {county_name}</p>
                <p style='margin: 2px 0;'><strong>FIPS Code:</strong> {fips_code}</p>
                <p style='margin: 2px 0;'><strong>Population:</strong> {row.get('population_2020', 'N/A'):,}</p>
                <p style='margin: 2px 0;'><strong>Area:</strong> {row.get('area_sq_miles', 'N/A'):.2f} sq mi</p>
                <p style='margin: 2px 0;'><strong>Boundary Type:</strong> TIGER/Line Data</p>
                <p style='margin: 2px 0;'><strong>Features:</strong> Real geographic boundaries</p>
            </div>
            """
            
            # Add municipality to map
            folium.GeoJson(
                row.geometry,
                style_function=lambda feature, color=county_color: {
                    'fillColor': color,
                    'color': color,
                    'weight': 2,
                    'fillOpacity': 0.7,
                    'opacity': 0.8
                },
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{row['NAME']} ({county_name})"
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        map_path = self.output_dir / 'tiger_municipal_boundaries_map.html'
        m.save(str(map_path))
        logger.info(f"TIGER/Line municipal boundaries map saved to {map_path}")
        
        return m
    
    def create_consolidation_map(self) -> Optional[folium.Map]:
        """Create a map showing consolidation scenarios."""
        logger.info("Creating consolidation scenario map...")
        
        # Load county boundaries
        counties_gdf = self.data_manager.load_tiger_counties()
        if counties_gdf is None or counties_gdf.empty:
            logger.error("No county data available for consolidation map")
            return None
        
        # Calculate map center
        center_lat = counties_gdf.geometry.centroid.y.mean()
        center_lon = counties_gdf.geometry.centroid.x.mean()
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=9,
            tiles='CartoDB dark_matter'
        )
        
        # Add county boundaries
        for _, row in counties_gdf.iterrows():
            county_name = self.data_manager.target_county_fips.get(row['COUNTYFP'], 'Unknown')
            county_color = self.county_colors.get(county_name, '#666666')
            
            # Create popup content
            popup_content = f"""
            <div style='color: white; background: #2d2d2d; padding: 10px; border-radius: 5px; width: 250px;'>
                <h4 style='color: {county_color}; margin: 0 0 5px 0;'>{county_name} County</h4>
                <p style='margin: 2px 0;'><strong>FIPS Code:</strong> {row['COUNTYFP']}</p>
                <p style='margin: 2px 0;'><strong>Consolidation Scenario:</strong> 5-County Boundary</p>
                <p style='margin: 2px 0;'><strong>Boundary Type:</strong> TIGER/Line County Data</p>
                <p style='margin: 2px 0;'><strong>Features:</strong> Real county boundaries</p>
            </div>
            """
            
            # Add county to map
            folium.GeoJson(
                row.geometry,
                style_function=lambda feature, color=county_color: {
                    'fillColor': color,
                    'color': color,
                    'weight': 3,
                    'fillOpacity': 0.3,
                    'opacity': 0.8
                },
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{county_name} County"
            ).add_to(m)
        
        # Add consolidation scenario markers
        consolidation_data = {
            '3-County Core': {
                'counties': ['Bergen', 'Essex', 'Hudson'],
                'color': '#ff6b35',
                'description': 'Core urban counties'
            },
            '5-County Boundary': {
                'counties': ['Bergen', 'Essex', 'Hudson', 'Passaic', 'Union'],
                'color': '#00d4ff',
                'description': 'Full Northern New Jersey region'
            }
        }
        
        for scenario_name, scenario_data in consolidation_data.items():
            folium.Marker(
                location=[center_lat + 0.1, center_lon + 0.1],
                popup=f"""
                <div style='color: white; background: #2d2d2d; padding: 10px; border-radius: 5px; width: 250px;'>
                    <h4 style='color: {scenario_data['color']}; margin: 0 0 5px 0;'>{scenario_name}</h4>
                    <p style='margin: 2px 0;'><strong>Counties:</strong> {', '.join(scenario_data['counties'])}</p>
                    <p style='margin: 2px 0;'><strong>Description:</strong> {scenario_data['description']}</p>
                </div>
                """,
                icon=folium.Icon(color='darkblue', icon='info-sign')
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        map_path = self.output_dir / 'tiger_consolidation_map.html'
        m.save(str(map_path))
        logger.info(f"TIGER/Line consolidation map saved to {map_path}")
        
        return m
    
    def create_all_maps(self) -> bool:
        """Create all TIGER/Line maps."""
        logger.info("Creating TIGER/Line boundary maps...")
        
        try:
            # Download and extract data if needed
            if not self.data_manager.download_tiger_data():
                logger.error("Failed to download TIGER data")
                return False
            
            if not self.data_manager.extract_tiger_data():
                logger.error("Failed to extract TIGER data")
                return False
            
            # Create maps
            municipalities_map = self.create_municipalities_map()
            consolidation_map = self.create_consolidation_map()
            
            if municipalities_map is None or consolidation_map is None:
                logger.error("Failed to create one or more maps")
                return False
            
            logger.info("All TIGER/Line maps saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating TIGER/Line maps: {e}")
            return False
