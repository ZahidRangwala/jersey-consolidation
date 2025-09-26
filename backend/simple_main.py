"""
Simple FastAPI Backend for New Jersey Consolidation Analysis
Serves basic data without requiring all files to exist
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import List, Dict, Any

app = FastAPI(title="New Jersey Consolidation Analysis API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8053"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "New Jersey Consolidation Analysis API"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/insights")
async def get_insights():
    """Get key insights and analysis results"""
    return {
        "total_population": 3610711,
        "us_rank": 3,
        "world_rank": 58,
        "municipalities_count": 142,
        "counties": ["Bergen", "Essex", "Hudson", "Passaic", "Union"]
    }

@app.get("/api/counties")
async def get_counties():
    """Get county summary data"""
    return [
        {
            "county": "Bergen",
            "population": 950000,
            "area_sq_miles": 234.5,
            "municipalities": 70,
            "population_density": 4051
        },
        {
            "county": "Essex", 
            "population": 850000,
            "area_sq_miles": 126.2,
            "municipalities": 22,
            "population_density": 6735
        },
        {
            "county": "Hudson",
            "population": 724854,
            "area_sq_miles": 46.2,
            "municipalities": 12,
            "population_density": 15689
        },
        {
            "county": "Passaic",
            "population": 524118,
            "area_sq_miles": 185.0,
            "municipalities": 16,
            "population_density": 2833
        },
        {
            "county": "Union",
            "population": 561719,
            "area_sq_miles": 103.0,
            "municipalities": 21,
            "population_density": 5454
        }
    ]

@app.get("/api/comparisons")
async def get_city_comparisons():
    """Get world city comparison data"""
    return [
        {"city": "Tokyo", "country": "Japan", "population": 37400068, "area_sq_km": 13572, "density_per_sq_km": 2755},
        {"city": "Delhi", "country": "India", "population": 32941000, "area_sq_km": 1484, "density_per_sq_km": 22200},
        {"city": "Shanghai", "country": "China", "population": 24870895, "area_sq_km": 6341, "density_per_sq_km": 3922},
        {"city": "Dhaka", "country": "Bangladesh", "population": 21741000, "area_sq_km": 306, "density_per_sq_km": 71049},
        {"city": "São Paulo", "country": "Brazil", "population": 12396372, "area_sq_km": 1521, "density_per_sq_km": 8148},
        {"city": "Cairo", "country": "Egypt", "population": 10230350, "area_sq_km": 606, "density_per_sq_km": 16882},
        {"city": "Mumbai", "country": "India", "population": 12478447, "area_sq_km": 603, "density_per_sq_km": 20694},
        {"city": "Beijing", "country": "China", "population": 21540000, "area_sq_km": 16410, "density_per_sq_km": 1312},
        {"city": "Osaka", "country": "Japan", "population": 19222665, "area_sq_km": 13193, "density_per_sq_km": 1457},
        {"city": "Chongqing", "country": "China", "population": 16382376, "area_sq_km": 82403, "density_per_sq_km": 199}
    ]

@app.get("/api/maps/municipal-boundaries")
async def get_municipal_boundaries_map():
    """Return the actual municipal boundaries map from TIGER/Line data"""
    try:
        map_path = Path("../visualizations/tiger_municipal_boundaries_map.html")
        if map_path.exists():
            with open(map_path, 'r', encoding='utf-8') as f:
                map_html = f.read()
            return {"html": map_html}
        else:
            # Fallback to other available maps
            fallback_paths = [
                "../visualizations/real_geographic_municipal_map.html",
                "../visualizations/real_municipal_boundaries_map.html",
                "../visualizations/improved_municipalities_map.html"
            ]
            
            for fallback_path in fallback_paths:
                if Path(fallback_path).exists():
                    with open(fallback_path, 'r', encoding='utf-8') as f:
                        map_html = f.read()
                    return {"html": map_html}
            
            # If no maps found, return placeholder
            return {
                "html": """
                <div style="width: 100%; height: 600px; background: #2d2d2d; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; border-radius: 8px;">
                    <div style="text-align: center;">
                        <h3 style="color: #00d4ff; margin-bottom: 20px;">Municipal Boundaries Map</h3>
                        <p>Map not found. Please generate maps first.</p>
                        <p style="color: #ff6b35; margin-top: 20px;">Your existing Dash dashboard is available at:</p>
                        <a href="http://localhost:8053" style="color: #00d4ff; text-decoration: none; font-weight: bold;">http://localhost:8053</a>
                    </div>
                </div>
                """
            }
    except Exception as e:
        return {
            "html": f"""
            <div style="width: 100%; height: 600px; background: #2d2d2d; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; border-radius: 8px;">
                <div style="text-align: center;">
                    <h3 style="color: #ff6b35; margin-bottom: 20px;">Error Loading Map</h3>
                    <p>Error: {str(e)}</p>
                    <p style="color: #00d4ff; margin-top: 20px;">Your existing Dash dashboard is available at:</p>
                    <a href="http://localhost:8053" style="color: #00d4ff; text-decoration: none; font-weight: bold;">http://localhost:8053</a>
                </div>
            </div>
            """
        }

@app.get("/api/maps/consolidation")
async def get_consolidation_map():
    """Return the actual consolidation scenarios map from TIGER/Line data"""
    try:
        # Use the newly generated TIGER consolidation map with proper L.geoJson boundaries and 3-county toggle
        map_path = Path("../visualizations/tiger_consolidation_map.html")
        if map_path.exists():
            with open(map_path, 'r', encoding='utf-8') as f:
                map_html = f.read()
            return {"html": map_html}
        else:
            # Fallback to other available consolidation maps
            fallback_paths = [
                "../visualizations/real_consolidation_map.html",
                "../visualizations/real_geographic_consolidation_map.html",
                "../visualizations/improved_consolidation_map.html"
            ]
            
            for fallback_path in fallback_paths:
                if Path(fallback_path).exists():
                    with open(fallback_path, 'r', encoding='utf-8') as f:
                        map_html = f.read()
                    return {"html": map_html}
            
            # If no maps found, return placeholder
            return {
                "html": """
                <div style="width: 100%; height: 600px; background: #2d2d2d; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; border-radius: 8px;">
                    <div style="text-align: center;">
                        <h3 style="color: #ff6b35; margin-bottom: 20px;">Consolidation Scenarios Map</h3>
                        <p>Map not found. Please generate maps first.</p>
                        <p style="color: #00d4ff; margin-top: 20px;">Your existing Dash dashboard is available at:</p>
                        <a href="http://localhost:8053" style="color: #00d4ff; text-decoration: none; font-weight: bold;">http://localhost:8053</a>
                    </div>
                </div>
                """
            }
    except Exception as e:
        return {
            "html": f"""
            <div style="width: 100%; height: 600px; background: #2d2d2d; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; border-radius: 8px;">
                <div style="text-align: center;">
                    <h3 style="color: #ff6b35; margin-bottom: 20px;">Error Loading Map</h3>
                    <p>Error: {str(e)}</p>
                    <p style="color: #00d4ff; margin-top: 20px;">Your existing Dash dashboard is available at:</p>
                    <a href="http://localhost:8053" style="color: #00d4ff; text-decoration: none; font-weight: bold;">http://localhost:8053</a>
                </div>
            </div>
            """
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
