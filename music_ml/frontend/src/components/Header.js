import React from 'react';
import { AppBar, Toolbar, Typography, Box, Tabs, Tab } from '@mui/material';
import SpotifyLoginButton from './SpotifyLoginButton';

const Header = ({ isAuthenticated, onLogoutSuccess }) => {
  return (
    <AppBar position="static" sx={{ backgroundColor: '#1c1c1c', marginBottom: 3 }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {/* Logo/Title */}
          <Typography variant="h4" component="div" sx={{ marginRight: 4 }}>
            mus
            <Typography
              component="span"
              variant="h4"
              sx={{ color: '#1DB954' }} // Spotify green for 'ai'
            >
              ai
            </Typography>
            c
          </Typography>

          {/* Navigation Tabs */}
          <Tabs 
            value={0} 
            textColor="inherit"
            sx={{
              '& .MuiTab-root': { 
                color: 'rgba(255,255,255,0.7)',
                '&.Mui-selected': { color: '#fff' }
              }
            }}
          >
            <Tab label="Playlist Generator" />
          </Tabs>
        </Box>

        {/* Login Button */}
        <SpotifyLoginButton 
          isAuthenticated={isAuthenticated}
          onLogoutSuccess={onLogoutSuccess}
        />
      </Toolbar>
    </AppBar>
  );
};

export default Header; 