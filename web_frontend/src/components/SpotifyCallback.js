import React, { useEffect } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/authService';

const SpotifyCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Log the full URL and search params
        console.log('Callback URL:', window.location.href);
        console.log('Location search:', location.search);
        
        // Get the parameters
        const params = new URLSearchParams(location.search);
        const error = params.get('error');
        const success = params.get('success');

        if (error) {
          console.error('Spotify auth error:', error);
          navigate('/');
          return;
        }

        if (!success) {
          console.error('Authentication not successful');
          navigate('/');
          return;
        }

        // Check if authentication was successful
        console.log('Checking auth status...');
        const isAuthenticated = await authService.checkAuthStatus();
        console.log('Auth status:', isAuthenticated);
        
        if (isAuthenticated) {
          navigate('/');
        } else {
          console.error('Authentication failed');
          navigate('/');
        }
      } catch (error) {
        console.error('Callback error:', error);
        navigate('/');
      }
    };

    handleCallback();
  }, [navigate, location]);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 4 }}>
      <CircularProgress sx={{ color: '#1DB954' }} />
      <Typography variant="h6" sx={{ mt: 2 }}>
        Completing Spotify login...
      </Typography>
    </Box>
  );
};

export default SpotifyCallback; 