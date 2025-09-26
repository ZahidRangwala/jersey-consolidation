import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Alert,
  CircularProgress,
  Chip,
} from '@mui/material';
import { TrendingUp, LocationCity, People, Public } from '@mui/icons-material';
import { apiService, Insights } from '../services/api';

const Dashboard: React.FC = () => {
  const [insights, setInsights] = useState<Insights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const data = await apiService.getInsights();
        setInsights(data);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Error fetching insights:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
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

  if (!insights) {
    return (
      <Alert severity="warning" sx={{ mt: 2 }}>
        No data available
      </Alert>
    );
  }

  const statCards = [
    {
      title: 'Total Population',
      value: insights.total_population.toLocaleString(),
      icon: <People sx={{ fontSize: 40 }} />,
      color: '#00d4ff',
    },
    {
      title: 'US City Rank',
      value: `#${insights.us_rank}`,
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: '#ff6b35',
    },
    {
      title: 'World City Rank',
      value: `#${insights.world_rank}`,
      icon: <Public sx={{ fontSize: 40 }} />,
      color: '#00ff88',
    },
    {
      title: 'Municipalities',
      value: insights.municipalities_count.toString(),
      icon: <LocationCity sx={{ fontSize: 40 }} />,
      color: '#9d4edd',
    },
  ];

  return (
    <Box>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          New Jersey Consolidation Analysis
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Exploring the potential for municipal consolidation in Northern New Jersey
        </Typography>
        <Alert severity="info" sx={{ mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Key Insight
          </Typography>
          <Typography>
            If Bergen, Essex, Hudson, Passaic, and Union counties were consolidated into one city, 
            it would rank <strong>#{insights.us_rank} in the United States</strong> with over{' '}
            <strong>{insights.total_population.toLocaleString()} people</strong>.
          </Typography>
        </Alert>
      </Box>

      {/* Statistics Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3, mb: 4 }}>
        {statCards.map((card, index) => (
          <Card key={index} sx={{ height: '100%', background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)' }}>
            <CardContent sx={{ textAlign: 'center', p: 3 }}>
              <Box sx={{ color: card.color, mb: 2 }}>
                {card.icon}
              </Box>
              <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
                {card.value}
              </Typography>
              <Typography variant="h6" color="text.secondary">
                {card.title}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>

      {/* Counties */}
      <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Target Counties
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {insights.counties.map((county, index) => {
              const colors = ['#00d4ff', '#ff6b35', '#00ff88', '#ffb347', '#9d4edd'];
              return (
                <Chip
                  key={county}
                  label={county}
                  sx={{
                    backgroundColor: colors[index % colors.length],
                    color: 'white',
                    fontWeight: 'bold',
                    '&:hover': {
                      backgroundColor: colors[index % colors.length],
                      opacity: 0.8,
                    },
                  }}
                />
              );
            })}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;