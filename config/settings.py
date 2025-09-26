"""
Configuration settings for the New Jersey Municipal Consolidation Analysis project.
"""

import os
from pathlib import Path
from typing import Dict, List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VISUALIZATIONS_DIR = PROJECT_ROOT / "visualizations"
TIGER_DATA_DIR = DATA_DIR / "tiger_data"
CONFIG_DIR = PROJECT_ROOT / "config"

# Target counties for Northern New Jersey analysis
TARGET_COUNTIES = ['Bergen', 'Essex', 'Hudson', 'Passaic', 'Union']

# New Jersey county FIPS codes for the 5 target counties
TARGET_COUNTY_FIPS = {
    '003': 'Bergen',    # Bergen County
    '005': 'Bergen',    # Bergen County (additional)
    '013': 'Essex',     # Essex County
    '017': 'Hudson',    # Hudson County
    '031': 'Passaic',   # Passaic County
    '039': 'Union'      # Union County
}

# County colors for visualization
COUNTY_COLORS = {
    'Bergen': '#00d4ff',
    'Essex': '#ff6b35', 
    'Hudson': '#00ff88',
    'Passaic': '#ffb347',
    'Union': '#9d4edd'
}

# TIGER/Line file URLs for New Jersey
TIGER_URLS = {
    'municipalities': 'https://www2.census.gov/geo/tiger/TIGER2023/PLACE/tl_2023_34_place.zip',
    'county_subdivisions': 'https://www2.census.gov/geo/tiger/TIGER2023/COUSUB/tl_2023_34_cousub.zip',
    'counties': 'https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip'
}

# New Jersey state data URLs (more comprehensive)
NJ_STATE_URLS = {
    'municipalities': 'https://www.nj.gov/dep/gis/digidownload/zips/statewide/Municipal_Boundaries_of_NJ.zip',
    'counties': 'https://www.nj.gov/dep/gis/digidownload/zips/statewide/County_Boundaries_of_NJ.zip'
}

# Dashboard settings
DASHBOARD_PORTS = {
    'main': 8051,
    'improved': 8053
}

# Analysis settings
CONSOLIDATION_SCENARIOS = {
    '3_county_core': {
        'name': '3-County Core',
        'counties': ['Bergen', 'Essex', 'Hudson'],
        'description': 'Core urban counties'
    },
    '5_county_boundary': {
        'name': '5-County Boundary',
        'counties': ['Bergen', 'Essex', 'Hudson', 'Passaic', 'Union'],
        'description': 'Full Northern New Jersey region'
    }
}

# Economic impact estimates
ECONOMIC_IMPACT = {
    'annual_savings_millions': 500,
    'efficiency_improvement_percent': 35,
    'government_reduction': '200+ → 1'
}

# Population and ranking data
POPULATION_DATA = {
    'consolidated_population': 3610711,
    'us_city_rank': 3,
    'world_city_rank': 58
}

# Create directories if they don't exist
def ensure_directories():
    """Ensure all required directories exist."""
    directories = [DATA_DIR, VISUALIZATIONS_DIR, TIGER_DATA_DIR, CONFIG_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': PROJECT_ROOT / 'logs' / 'nj_consolidation.log',
            'mode': 'a',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
