import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Container, AppBar, Toolbar, Typography, Tabs, Tab } from '@mui/material';
import Dashboard from './components/Dashboard';
import Maps from './components/Maps';
import Analysis from './components/Analysis';
import './App.css';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00d4ff',
    },
    secondary: {
      main: '#ff6b35',
    },
    background: {
      default: '#1a1a1a',
      paper: '#2d2d2d',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" sx={{ background: 'linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%)' }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              New Jersey Consolidation Analysis
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth={false} sx={{ mt: 2, px: 2 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="navigation tabs">
              <Tab label="Maps" />
              <Tab label="Dashboard" />
              <Tab label="Analysis" />
            </Tabs>
          </Box>
          
          <TabPanel value={value} index={0}>
            <Maps />
          </TabPanel>
          <TabPanel value={value} index={1}>
            <Dashboard />
          </TabPanel>
          <TabPanel value={value} index={2}>
            <Analysis />
          </TabPanel>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;