"""
FastAPI Backend for New Jersey Consolidation Analysis
Serves data from existing Python analysis to React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import pandas as pd
import json
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

from tiger_boundaries import TIGERBoundaryCreator
from visualizations import NJVisualizationCreator

app = FastAPI(title="New Jersey Consolidation Analysis API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8053"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated maps (create directory if it doesn't exist)
import os
visualizations_dir = Path("../visualizations")
visualizations_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(visualizations_dir)), name="static")

# Initialize data creators
tiger_creator = TIGERBoundaryCreator()
viz_creator = NJVisualizationCreator()

@app.get("/")
async def root():
    return {"message": "New Jersey Consolidation Analysis API"}

@app.get("/api/municipalities")
async def get_municipalities():
    """Get all municipalities data"""
    try:
        municipalities_df = pd.read_csv("../data/nj_municipalities.csv")
        return municipalities_df.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Municipalities data not found")

@app.get("/api/municipalities/target-region")
async def get_target_region_municipalities():
    """Get municipalities in the target 5-county region"""
    try:
        municipalities_df = pd.read_csv("../data/nj_municipalities.csv")
        target_region = municipalities_df[municipalities_df['in_target_region'] == True]
        return target_region.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Municipalities data not found")

@app.get("/api/counties")
async def get_counties():
    """Get county summary data"""
    try:
        municipalities_df = pd.read_csv("../data/nj_municipalities.csv")
        target_region = municipalities_df[municipalities_df['in_target_region'] == True]
        
        county_summary = target_region.groupby('county').agg({
            'population_2020': 'sum',
            'area_sq_miles': 'sum',
            'municipality': 'count'
        }).reset_index()
        
        county_summary.columns = ['county', 'population', 'area_sq_miles', 'municipalities']
        county_summary['population_density'] = county_summary['population'] / county_summary['area_sq_miles']
        
        return county_summary.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Municipalities data not found")

@app.get("/api/scenarios")
async def get_consolidation_scenarios():
    """Get consolidation scenarios data"""
    try:
        scenarios_df = pd.read_csv("../data/consolidation_scenarios.csv")
        return scenarios_df.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Scenarios data not found")

@app.get("/api/comparisons")
async def get_city_comparisons():
    """Get world city comparison data"""
    try:
        comparisons_df = pd.read_csv("../data/city_comparisons.csv")
        return comparisons_df.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="City comparisons data not found")

@app.get("/api/economic-impact")
async def get_economic_impact():
    """Get economic impact data"""
    try:
        economic_df = pd.read_csv("../data/economic_impact.csv")
        return economic_df.to_dict("records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Economic impact data not found")

@app.get("/api/maps/municipal-boundaries")
async def get_municipal_boundaries_map():
    """Generate and return municipal boundaries map"""
    try:
        # Use the improved municipalities map which has proper boundaries
        map_path = Path("../visualizations/improved_municipalities_map.html")
        if not map_path.exists():
            # Fallback to tiger map if improved doesn't exist
            map_path = Path("../visualizations/tiger_municipal_boundaries_map.html")
            if not map_path.exists():
                tiger_creator.create_tiger_municipalities_map()
        
        # Return the map HTML content
        with open(map_path, 'r') as f:
            map_html = f.read()
        
        return {"html": map_html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating map: {str(e)}")

@app.get("/api/maps/consolidation")
async def get_consolidation_map():
    """Generate and return consolidation scenarios map"""
    try:
        # Use the real consolidation map which has both proper county boundaries and working 3-county toggle
        map_path = Path("../visualizations/real_consolidation_map.html")
        if not map_path.exists():
            # Fallback to other available maps
            fallback_paths = [
                "../visualizations/real_geographic_consolidation_map.html",
                "../visualizations/improved_consolidation_map.html",
                "../visualizations/tiger_consolidation_map.html"
            ]
            for fallback_path in fallback_paths:
                if Path(fallback_path).exists():
                    map_path = Path(fallback_path)
                    break
        
        # Return the map HTML content
        with open(map_path, 'r') as f:
            map_html = f.read()
        
        return {"html": map_html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating map: {str(e)}")

@app.get("/api/insights")
async def get_insights():
    """Get key insights and analysis results"""
    try:
        with open("../data/analysis_insights.json", 'r') as f:
            insights = json.load(f)
        return insights
    except FileNotFoundError:
        # Return default insights if file doesn't exist
        return {
            "total_population": 3610711,
            "us_rank": 3,
            "world_rank": 58,
            "municipalities_count": 142,
            "counties": ["Bergen", "Essex", "Hudson", "Passaic", "Union"]
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
