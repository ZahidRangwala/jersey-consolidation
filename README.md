# New Jersey Consolidation Visualization Project

A comprehensive data visualization project exploring the potential for municipal consolidation in Northern New Jersey, inspired by the concept of creating a "Greater Jersey City" that would become the third largest city in the United States.

## Project Overview

This project analyzes the fragmented municipal structure of Northern New Jersey and visualizes the potential benefits of consolidation, including:

- **Population Analysis**: Current vs. consolidated population scenarios
- **Geographic Visualization**: Interactive maps showing municipal boundaries
- **Economic Impact**: Cost savings and efficiency gains from consolidation
- **Comparative Analysis**: How a consolidated NJ would rank among world cities
- **Demographic Insights**: Population distribution and density analysis

## Key Findings

- Northern New Jersey (5 counties) has **3,610,711 people** across hundreds of municipalities
- If consolidated, it would be the **3rd largest city in the US** (after NYC and LA)
- Would rank **58th globally**, ahead of Madrid, Buenos Aires, and Toronto
- Current fragmentation leads to inefficient government spending and infrastructure

## Project Structure

```
jersey/
├── data/                    # Raw and processed datasets
├── notebooks/              # Jupyter notebooks for analysis
├── src/                    # Source code modules
├── visualizations/         # Generated charts and maps
├── dashboard/              # Interactive Dash application
└── docs/                   # Documentation and reports
```

## Technologies Used

- **Python**: Data processing and analysis
- **Pandas/NumPy**: Data manipulation
- **Plotly/Dash**: Interactive visualizations and dashboard
- **GeoPandas/Folium**: Geographic data and mapping
- **Matplotlib/Seaborn**: Statistical visualizations

## Quick Start

### Option 1: Run Demo (Recommended for first-time users)
```bash
python run_demo.py
```

### Option 2: Full Pipeline
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete analysis pipeline
python main.py

# Launch interactive dashboard
python main.py --dashboard
```

### Option 3: Step-by-Step
```bash
# 1. Collect data
python src/data_collection.py

# 2. Run analysis
python src/analysis.py

# 3. Generate visualizations
python src/visualizations.py

# 4. Launch dashboard
python dashboard/app.py
```

### Option 4: Jupyter Notebook
```bash
jupyter notebook notebooks/nj_consolidation_analysis.ipynb
```

## Data Sources

- US Census Bureau (population, demographics)
- New Jersey Department of State (municipal boundaries)
- OpenStreetMap (geographic data)
- Various NJ government datasets

## Inspiration

This project is inspired by the article ["New Jersey's Potential and a Plea for a Greater Jersey City"](https://papaghanoush.substack.com/p/new-jerseys-potential-and-a-plea) by Matty Monahan, which explores the concept of consolidating Northern New Jersey's municipalities into a single, more efficient city.

## Project Features

### 📊 Data Analysis
- **Population Analysis**: Current vs. consolidated population scenarios
- **Geographic Analysis**: County and municipality breakdowns
- **Economic Impact**: Cost savings and efficiency projections
- **Comparative Analysis**: Rankings against US and world cities

### 📈 Visualizations
- **Interactive Charts**: Population comparisons, world rankings
- **Economic Gauges**: Efficiency improvement metrics
- **Geographic Maps**: County and municipality distributions
- **Size Analysis**: Municipality size distribution patterns

### 🚀 Interactive Dashboard
- **Multi-tab Interface**: Organized analysis sections
- **Real-time Updates**: Dynamic data exploration
- **Responsive Design**: Works on desktop and mobile
- **Export Capabilities**: Save charts and data

### 📚 Documentation
- **Methodology Guide**: Detailed analysis approach
- **Visualization Guide**: Chart interpretation help
- **Jupyter Notebooks**: Step-by-step analysis
- **Code Documentation**: Comprehensive inline comments

## Key Insights

Based on the analysis, a consolidated Northern New Jersey would:

- **Population**: 3,610,711 people (3rd largest US city)
- **Global Ranking**: 58th largest world city
- **Economic Savings**: ~$500 million annually
- **Government Reduction**: 200+ municipalities → 1
- **Efficiency Gains**: 30-40% improvement in key metrics

## File Structure

```
jersey/
├── main.py                    # Main execution script
├── run_demo.py               # Quick demo script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # Generated datasets
│   ├── nj_municipalities.csv
│   ├── consolidation_scenarios.csv
│   ├── city_comparisons.csv
│   └── economic_impact.csv
├── src/                      # Source code modules
│   ├── data_collection.py    # Data gathering and processing
│   ├── analysis.py          # Statistical analysis
│   └── visualizations.py    # Chart generation
├── dashboard/                # Interactive dashboard
│   └── app.py               # Dash application
├── notebooks/                # Jupyter notebooks
│   └── nj_consolidation_analysis.ipynb
├── visualizations/           # Generated charts
│   ├── population_comparison.html
│   ├── world_city_ranking.html
│   ├── county_analysis.html
│   ├── economic_impact.html
│   └── municipality_size_distribution.html
└── docs/                     # Documentation
    ├── analysis_methodology.md
    └── visualization_guide.md
```

## Customization

### Adding New Data Sources
1. Modify `src/data_collection.py` to include new datasets
2. Update analysis methods in `src/analysis.py`
3. Add new visualizations in `src/visualizations.py`

### Extending the Dashboard
1. Add new tabs in `dashboard/app.py`
2. Create corresponding callback functions
3. Update the layout and styling

### Modifying Visualizations
1. Edit chart configurations in `src/visualizations.py`
2. Adjust color schemes and styling
3. Add new chart types as needed

## Contributing

This project is designed for learning and portfolio development. Feel free to:
- Fork and modify for your own analysis
- Add new data sources or visualizations
- Improve the dashboard interface
- Extend the analysis methodology

## License

MIT License - feel free to use this project for your own data visualization learning and portfolio development.

## Acknowledgments

- Inspired by [New Jersey's Potential and a Plea for a Greater Jersey City](https://papaghanoush.substack.com/p/new-jerseys-potential-and-a-plea)
- Data sources: US Census Bureau, New Jersey Department of State
- Visualization libraries: Plotly, Dash, Matplotlib, Seaborn
