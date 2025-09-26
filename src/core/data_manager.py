"""
Core data management module for the New Jersey Municipal Consolidation Analysis.
Handles data collection, processing, and validation.
"""

import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
import zipfile
import shutil

from config.settings import (
    DATA_DIR, TIGER_DATA_DIR, TARGET_COUNTIES, TARGET_COUNTY_FIPS,
    TIGER_URLS, NJ_STATE_URLS
)

logger = logging.getLogger(__name__)


class DataManager:
    """Manages all data operations for the NJ consolidation analysis."""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.tiger_dir = TIGER_DATA_DIR
        self.target_counties = TARGET_COUNTIES
        self.target_county_fips = TARGET_COUNTY_FIPS
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tiger_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("DataManager initialized")
    
    def download_tiger_data(self) -> bool:
        """Download TIGER/Line files from US Census Bureau."""
        logger.info("Downloading TIGER/Line files from US Census Bureau...")
        
        success = True
        for data_type, url in TIGER_URLS.items():
            zip_path = self.tiger_dir / f"{data_type}.zip"
            
            if not zip_path.exists():
                logger.info(f"Downloading {data_type} data...")
                try:
                    response = requests.get(url, stream=True, verify=False)
                    response.raise_for_status()
                    
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    logger.info(f"Downloaded {data_type} data successfully")
                except Exception as e:
                    logger.error(f"Error downloading {data_type} data: {e}")
                    success = False
            else:
                logger.info(f"{data_type} data already exists")
        
        return success
    
    def extract_tiger_data(self) -> bool:
        """Extract downloaded TIGER/Line zip files."""
        logger.info("Extracting TIGER/Line files...")
        
        success = True
        for data_type in TIGER_URLS.keys():
            zip_path = self.tiger_dir / f"{data_type}.zip"
            extract_dir = self.tiger_dir / data_type
            
            if zip_path.exists() and not extract_dir.exists():
                logger.info(f"Extracting {data_type} data...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    logger.info(f"Extracted {data_type} data successfully")
                except Exception as e:
                    logger.error(f"Error extracting {data_type} data: {e}")
                    success = False
            else:
                logger.info(f"{data_type} data already extracted")
        
        return success
    
    def load_tiger_municipalities(self) -> Optional[gpd.GeoDataFrame]:
        """Load TIGER/Line municipal boundary data for New Jersey."""
        logger.info("Loading TIGER/Line municipal boundary data...")
        
        municipalities_dir = self.tiger_dir / 'municipalities'
        shapefile_path = None
        
        # Find the shapefile
        for file in municipalities_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            logger.error("No municipal shapefile found")
            return None
        
        try:
            gdf = gpd.read_file(shapefile_path)
            logger.info(f"Loaded {len(gdf)} municipalities from TIGER/Line data")
            
            # Filter to only include municipalities from the 5 target counties
            if 'COUNTYFP' in gdf.columns:
                gdf = gdf[gdf['COUNTYFP'].isin(self.target_county_fips.keys())]
                logger.info(f"Filtered to {len(gdf)} municipalities in 5 target counties")
            else:
                logger.warning("COUNTYFP column not found, cannot filter by county")
            
            return gdf
            
        except Exception as e:
            logger.error(f"Error loading TIGER/Line municipal data: {e}")
            return None
    
    def load_tiger_county_subdivisions(self) -> Optional[gpd.GeoDataFrame]:
        """Load TIGER/Line county subdivision data for New Jersey."""
        logger.info("Loading TIGER/Line county subdivision data...")
        
        cousub_dir = self.tiger_dir / 'county_subdivisions'
        shapefile_path = None
        
        # Find the shapefile
        for file in cousub_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            logger.error("No county subdivision shapefile found")
            return None
        
        try:
            gdf = gpd.read_file(shapefile_path)
            logger.info(f"Loaded {len(gdf)} county subdivisions from TIGER/Line data")
            
            # Filter to only include county subdivisions from the 5 target counties
            if 'COUNTYFP' in gdf.columns:
                gdf = gdf[gdf['COUNTYFP'].isin(self.target_county_fips.keys())]
                logger.info(f"Filtered to {len(gdf)} county subdivisions in 5 target counties")
            else:
                logger.warning("COUNTYFP column not found, cannot filter by county")
            
            return gdf
            
        except Exception as e:
            logger.error(f"Error loading TIGER/Line county subdivision data: {e}")
            return None
    
    def load_tiger_counties(self) -> Optional[gpd.GeoDataFrame]:
        """Load TIGER/Line county boundary data for New Jersey."""
        logger.info("Loading TIGER/Line county boundary data...")
        
        counties_dir = self.tiger_dir / 'counties'
        shapefile_path = None
        
        # Find the shapefile
        for file in counties_dir.glob('*.shp'):
            shapefile_path = file
            break
        
        if not shapefile_path:
            logger.error("No county shapefile found")
            return None
        
        try:
            gdf = gpd.read_file(shapefile_path)
            logger.info(f"Loaded {len(gdf)} counties from TIGER/Line data")
            
            # Filter to New Jersey counties (STATEFP = '34')
            gdf = gdf[gdf['STATEFP'] == '34']
            logger.info(f"Filtered to {len(gdf)} counties in New Jersey")
            
            # Filter to target counties
            target_fips = list(self.target_county_fips.keys())
            gdf = gdf[gdf['COUNTYFP'].isin(target_fips)]
            logger.info(f"Filtered to {len(gdf)} target counties in New Jersey")
            
            return gdf
            
        except Exception as e:
            logger.error(f"Error loading TIGER/Line county data: {e}")
            return None
    
    def create_comprehensive_municipalities_dataset(self) -> pd.DataFrame:
        """Create a comprehensive dataset of Northern NJ municipalities."""
        logger.info("Creating comprehensive Northern NJ municipalities dataset...")
        
        # This would contain the comprehensive list of municipalities
        # For now, we'll load from the existing CSV
        csv_path = self.data_dir / 'nj_municipalities.csv'
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} municipalities from CSV")
            return df
        else:
            logger.warning("Municipalities CSV not found, creating empty dataset")
            return pd.DataFrame(columns=['municipality', 'county', 'population_2020', 'area_sq_miles'])
    
    def validate_data_quality(self, gdf: gpd.GeoDataFrame, data_type: str) -> Dict[str, any]:
        """Validate the quality of loaded geographic data."""
        logger.info(f"Validating {data_type} data quality...")
        
        validation_results = {
            'total_records': len(gdf),
            'valid_geometries': gdf.geometry.is_valid.sum(),
            'null_geometries': gdf.geometry.isnull().sum(),
            'crs': str(gdf.crs) if gdf.crs else 'No CRS',
            'bounds': gdf.total_bounds.tolist() if not gdf.empty else None
        }
        
        # Check for common issues
        if validation_results['null_geometries'] > 0:
            logger.warning(f"Found {validation_results['null_geometries']} null geometries")
        
        if not gdf.geometry.is_valid.all():
            invalid_count = (~gdf.geometry.is_valid).sum()
            logger.warning(f"Found {invalid_count} invalid geometries")
        
        logger.info(f"Data validation complete: {validation_results}")
        return validation_results
