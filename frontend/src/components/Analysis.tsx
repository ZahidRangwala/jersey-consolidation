import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardHeader,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { apiService, County, CityComparison } from '../services/api';

const Analysis: React.FC = () => {
  const [counties, setCounties] = useState<County[]>([]);
  const [cityComparisons, setCityComparisons] = useState<CityComparison[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysisData = async () => {
      try {
        setLoading(true);
        const [countiesData, comparisonsData] = await Promise.all([
          apiService.getCounties(),
          apiService.getCityComparisons(),
        ]);
        
        setCounties(countiesData);
        setCityComparisons(comparisonsData.slice(0, 10)); // Top 10 cities
      } catch (err) {
        setError('Failed to load analysis data');
        console.error('Error fetching analysis data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysisData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  const countyColors = ['#00d4ff', '#ff6b35', '#00ff88', '#ffb347', '#9d4edd'];

  const pieData = counties.map((county, index) => ({
    name: county.county,
    value: county.population,
    color: countyColors[index % countyColors.length],
  }));

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Data Analysis
      </Typography>

      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: 3, mb: 3 }}>
        {/* County Analysis */}
        <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)' }}>
          <CardHeader
            title="Population by County"
            sx={{ 
              background: 'linear-gradient(90deg, #00d4ff 0%, #0099cc 100%)',
              color: 'white',
              '& .MuiCardHeader-title': {
                fontSize: '1.25rem',
                fontWeight: 600,
              }
            }}
          />
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={counties}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="county" stroke="#fff" />
                <YAxis stroke="#fff" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#2d2d2d', 
                    border: '1px solid #555',
                    color: '#fff'
                  }} 
                />
                <Bar dataKey="population" fill="#00d4ff" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* County Distribution Pie Chart */}
        <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)' }}>
          <CardHeader
            title="Population Distribution"
            sx={{ 
              background: 'linear-gradient(90deg, #ff6b35 0%, #cc5529 100%)',
              color: 'white',
              '& .MuiCardHeader-title': {
                fontSize: '1.25rem',
                fontWeight: 600,
              }
            }}
          />
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#2d2d2d', 
                    border: '1px solid #555',
                    color: '#fff'
                  }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Box>

      {/* County Details Table */}
      <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', mb: 3 }}>
        <CardHeader
          title="County Analysis Details"
          sx={{ 
            background: 'linear-gradient(90deg, #00ff88 0%, #00cc6a 100%)',
            color: 'white',
            '& .MuiCardHeader-title': {
              fontSize: '1.25rem',
              fontWeight: 600,
            }
          }}
        />
        <CardContent>
          <TableContainer component={Paper} sx={{ backgroundColor: '#1a1a1a' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>County</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Population</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Area (sq mi)</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Density</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Municipalities</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {counties.map((county, index) => (
                  <TableRow key={county.county}>
                    <TableCell sx={{ color: '#fff' }}>
                      <Chip
                        label={county.county}
                        sx={{
                          backgroundColor: countyColors[index % countyColors.length],
                          color: 'white',
                          fontWeight: 'bold',
                        }}
                      />
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {county.population.toLocaleString()}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {county.area_sq_miles.toFixed(1)}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {county.population_density.toFixed(0)}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {county.municipalities}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* World City Comparisons */}
      <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)' }}>
        <CardHeader
          title="World City Rankings"
          sx={{ 
            background: 'linear-gradient(90deg, #9d4edd 0%, #7b2cbf 100%)',
            color: 'white',
            '& .MuiCardHeader-title': {
              fontSize: '1.25rem',
              fontWeight: 600,
            }
          }}
        />
        <CardContent>
          <TableContainer component={Paper} sx={{ backgroundColor: '#1a1a1a' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>City</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Country</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Population</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Area (sq km)</TableCell>
                  <TableCell align="right" sx={{ color: '#fff', fontWeight: 'bold' }}>Density</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {cityComparisons.map((city, index) => (
                  <TableRow key={city.city}>
                    <TableCell sx={{ color: '#fff' }}>
                      {city.city}
                    </TableCell>
                    <TableCell sx={{ color: '#fff' }}>
                      {city.country}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {city.population.toLocaleString()}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {city.area_sq_km.toLocaleString()}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#fff' }}>
                      {city.density_per_sq_km.toLocaleString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Analysis;