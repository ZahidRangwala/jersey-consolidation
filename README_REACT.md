# New Jersey Consolidation Analysis - React Frontend

This is the modern React frontend for the New Jersey Consolidation Analysis project, replacing the previous Dash-based interface with a more modern, responsive, and interactive user experience.

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) v5
- **Charts**: Recharts
- **Maps**: Embedded Folium maps (from Python backend)
- **HTTP Client**: Axios
- **Styling**: Custom CSS with dark theme

### Backend (FastAPI)
- **Framework**: FastAPI
- **Data Processing**: Pandas, GeoPandas
- **Maps**: Folium (existing TIGER/Line integration)
- **CORS**: Enabled for React frontend

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the development startup script
./start_dev.sh
```

This will:
- Install all dependencies
- Start the FastAPI backend on http://localhost:8000
- Start the React frontend on http://localhost:3000

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📱 Features

### Dashboard
- **Key Statistics**: Population, US rank, world rank, municipality count
- **Interactive Cards**: Hover effects and animations
- **County Overview**: Color-coded county chips
- **Key Insights**: Highlighted consolidation benefits

### Maps
- **Current Municipal Structure**: Interactive map with black outlines and county color coding
- **Consolidation Scenarios**: 5-county and 3-county consolidation options
- **Tabbed Interface**: Easy switching between map views
- **Responsive Design**: Works on desktop, tablet, and mobile

### Analysis
- **County Analysis**: Population distribution charts and detailed tables
- **World City Rankings**: Comparison with global cities
- **Interactive Charts**: Bar charts, pie charts, and data tables
- **Export Ready**: All data available via API

## 🔧 API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /api/municipalities` - All municipalities data
- `GET /api/municipalities/target-region` - Target 5-county region municipalities
- `GET /api/counties` - County summary statistics
- `GET /api/scenarios` - Consolidation scenarios
- `GET /api/comparisons` - World city comparisons
- `GET /api/economic-impact` - Economic impact data
- `GET /api/maps/municipal-boundaries` - Municipal boundaries map HTML
- `GET /api/maps/consolidation` - Consolidation scenarios map HTML
- `GET /api/insights` - Key insights and analysis results

## 🎨 Design Features

### Dark Theme
- Professional dark color scheme
- High contrast for accessibility
- Gradient accents for visual appeal

### Responsive Design
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly controls

### Interactive Elements
- Hover effects on cards and buttons
- Smooth transitions and animations
- Loading states and error handling

### Color Coding
- **Bergen**: Light Blue (#00d4ff)
- **Essex**: Orange (#ff6b35)
- **Hudson**: Green (#00ff88)
- **Passaic**: Light Orange (#ffb347)
- **Union**: Purple (#9d4edd)

## 📊 Data Integration

The React frontend seamlessly integrates with your existing Python analysis:

- **Municipal Boundaries**: Uses existing TIGER/Line data processing
- **Population Data**: Leverages comprehensive municipalities dataset
- **Consolidation Scenarios**: Integrates with existing scenario analysis
- **Visualizations**: Maintains all existing chart and map functionality

## 🔄 Migration Benefits

### From Dash to React:
- **Better Performance**: Faster rendering and interactions
- **Modern UI**: Material-UI components and design patterns
- **Responsive Design**: Better mobile and tablet experience
- **Maintainability**: Cleaner component architecture
- **Extensibility**: Easy to add new features and integrations

### Preserved Functionality:
- ✅ All existing maps and visualizations
- ✅ Municipal boundary data with black outlines
- ✅ County color coding
- ✅ Population and demographic data
- ✅ Consolidation scenario analysis
- ✅ World city comparisons

## 🛠️ Development

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── Maps.tsx
│   │   └── Analysis.tsx
│   ├── services/
│   │   └── api.ts
│   ├── App.tsx
│   └── App.css
├── public/
└── package.json

backend/
├── main.py
├── requirements.txt
└── venv/
```

### Adding New Features
1. **Backend**: Add new endpoints in `backend/main.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **API Integration**: Update `frontend/src/services/api.ts`
4. **Styling**: Add custom styles in `frontend/src/App.css`

## 🌐 Deployment

### Development
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production
- Build frontend: `npm run build`
- Serve static files from FastAPI
- Deploy to cloud platform (Heroku, AWS, etc.)

## 📝 Notes

- The React frontend maintains full compatibility with your existing data and analysis
- All maps are generated using the existing Python/Folium pipeline
- The interface is designed to be professional and suitable for presentations
- The dark theme provides excellent contrast for data visualization
- All interactive features are preserved and enhanced

## 🎯 Next Steps

1. **Enhanced Maps**: Consider integrating Mapbox GL JS for more interactive maps
2. **Real-time Data**: Add data refresh capabilities
3. **Export Features**: Add PDF/Excel export functionality
4. **User Preferences**: Add theme switching and customization options
5. **Mobile App**: Consider React Native for mobile applications
