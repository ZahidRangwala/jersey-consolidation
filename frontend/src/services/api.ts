import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Municipality {
  municipality: string;
  county: string;
  population_2020: number;
  area_sq_miles: number;
  population_density: number;
  in_target_region: boolean;
}

export interface County {
  county: string;
  population: number;
  area_sq_miles: number;
  municipalities: number;
  population_density: number;
}

export interface ConsolidationScenario {
  scenario: string;
  population: number;
  municipalities: number;
  us_rank: number;
  world_rank: number;
}

export interface CityComparison {
  city: string;
  country: string;
  population: number;
  area_sq_km: number;
  density_per_sq_km: number;
}

export interface EconomicImpact {
  category: string;
  improvement_percentage: number;
  description: string;
}

export interface Insights {
  total_population: number;
  us_rank: number;
  world_rank: number;
  municipalities_count: number;
  counties: string[];
}

export const apiService = {
  // Municipalities
  getMunicipalities: async (): Promise<Municipality[]> => {
    const response = await api.get('/api/municipalities');
    return response.data;
  },

  getTargetRegionMunicipalities: async (): Promise<Municipality[]> => {
    const response = await api.get('/api/municipalities/target-region');
    return response.data;
  },

  // Counties
  getCounties: async (): Promise<County[]> => {
    const response = await api.get('/api/counties');
    return response.data;
  },

  // Scenarios
  getConsolidationScenarios: async (): Promise<ConsolidationScenario[]> => {
    const response = await api.get('/api/scenarios');
    return response.data;
  },

  // Comparisons
  getCityComparisons: async (): Promise<CityComparison[]> => {
    const response = await api.get('/api/comparisons');
    return response.data;
  },

  // Economic Impact
  getEconomicImpact: async (): Promise<EconomicImpact[]> => {
    const response = await api.get('/api/economic-impact');
    return response.data;
  },

  // Maps
  getMunicipalBoundariesMap: async (): Promise<{ html: string }> => {
    const response = await api.get('/api/maps/municipal-boundaries');
    return response.data;
  },

  getConsolidationMap: async (): Promise<{ html: string }> => {
    const response = await api.get('/api/maps/consolidation');
    return response.data;
  },

  // Insights
  getInsights: async (): Promise<Insights> => {
    const response = await api.get('/api/insights');
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; message: string }> => {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default apiService;
