import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardHeader,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import { apiService } from '../services/api';


const Maps: React.FC = () => {
  const [municipalMapHtml, setMunicipalMapHtml] = useState<string>('');
  const [consolidationMapHtml, setConsolidationMapHtml] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMaps = async () => {
      try {
        setLoading(true);
        const [municipalResponse, consolidationResponse] = await Promise.all([
          apiService.getMunicipalBoundariesMap(),
          apiService.getConsolidationMap(),
        ]);
        
        console.log('Municipal map HTML length:', municipalResponse.html.length);
        console.log('Consolidation map HTML length:', consolidationResponse.html.length);
        console.log('Municipal map HTML preview:', municipalResponse.html.substring(0, 200));
        console.log('Consolidation map HTML preview:', consolidationResponse.html.substring(0, 200));
        setMunicipalMapHtml(municipalResponse.html);
        setConsolidationMapHtml(consolidationResponse.html);
      } catch (err) {
        setError('Failed to load maps');
        console.error('Error fetching maps:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMaps();
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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Interactive Maps
      </Typography>
      
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 3, height: '800px' }}>
        {/* Current Municipal Structure Map */}
        <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', height: '100%' }}>
          <CardHeader
            title="Current Municipal Structure"
            sx={{ 
              background: 'linear-gradient(90deg, #00d4ff 0%, #0099cc 100%)',
              color: 'white',
              '& .MuiCardHeader-title': {
                fontSize: '1.25rem',
                fontWeight: 600,
              }
            }}
          />
          <CardContent sx={{ p: 0, height: 'calc(100% - 64px)' }}>
            <Box
              sx={{
                height: '100%',
                width: '100%',
                '& iframe': {
                  width: '100%',
                  height: '100%',
                  border: 'none',
                },
              }}
            >
              {municipalMapHtml ? (
                <Box sx={{ height: '100%', position: 'relative' }}>
                  <iframe
                    srcDoc={municipalMapHtml}
                    style={{ width: '100%', height: '100%', border: 'none' }}
                    title="Municipal Boundaries Map"
                    onLoad={() => console.log('Municipal map iframe loaded')}
                    onError={() => console.log('Municipal map iframe error')}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 10,
                      right: 10,
                      background: 'rgba(0,0,0,0.7)',
                      color: 'white',
                      padding: '5px 10px',
                      borderRadius: '4px',
                      fontSize: '12px',
                    }}
                  >
                    Interactive Map
                  </Box>
                </Box>
              ) : (
                <Box
                  sx={{
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px',
                  }}
                >
                  Loading map...
                </Box>
              )}
            </Box>
          </CardContent>
        </Card>

        {/* Consolidation Scenarios Map */}
        <Card sx={{ background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', height: '100%' }}>
          <CardHeader
            title="Consolidation Scenarios"
            sx={{ 
              background: 'linear-gradient(90deg, #ff6b35 0%, #cc5529 100%)',
              color: 'white',
              '& .MuiCardHeader-title': {
                fontSize: '1.25rem',
                fontWeight: 600,
              }
            }}
          />
          <CardContent sx={{ p: 0, height: 'calc(100% - 64px)' }}>
            <Box
              sx={{
                height: '100%',
                width: '100%',
                '& iframe': {
                  width: '100%',
                  height: '100%',
                  border: 'none',
                },
              }}
            >
              {consolidationMapHtml ? (
                <Box sx={{ height: '100%', position: 'relative' }}>
                  <iframe
                    srcDoc={consolidationMapHtml}
                    style={{ width: '100%', height: '100%', border: 'none' }}
                    title="Consolidation Scenarios Map"
                    onLoad={() => console.log('Consolidation map iframe loaded')}
                    onError={() => console.log('Consolidation map iframe error')}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 10,
                      right: 10,
                      background: 'rgba(0,0,0,0.7)',
                      color: 'white',
                      padding: '5px 10px',
                      borderRadius: '4px',
                      fontSize: '12px',
                    }}
                  >
                    Interactive Map
                  </Box>
                </Box>
              ) : (
                <Box
                  sx={{
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px',
                  }}
                >
                  Loading map...
                </Box>
              )}
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default Maps;
