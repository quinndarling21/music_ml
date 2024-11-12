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
        console.log('Callback URL:', window.location.href);
        console.log('Location search:', location.search);
        
        const params = new URLSearchParams(location.search);
        const error = params.get('error');
        const code = params.get('code');

        if (error) {
          console.error('Spotify auth error:', error);
          navigate('/?error=' + encodeURIComponent(error));
          return;
        }

        if (!code) {
          console.error('No authorization code received');
          navigate('/?error=no_code');
          return;
        }

        console.log('Processing authorization code...');
        const response = await authService.processCallback(code);
        console.log('Callback response:', response);

        if (response.success) {
          console.log('Checking auth status...');
          const isAuthenticated = await authService.checkAuthStatus();
          console.log('Auth status:', isAuthenticated);
          
          if (isAuthenticated) {
            navigate('/?success=true');
          } else {
            console.error('Authentication failed');
            navigate('/?error=auth_failed');
          }
        } else {
          console.error('Callback processing failed');
          navigate('/?error=callback_failed');
        }
      } catch (error) {
        console.error('Callback error:', error);
        navigate('/?error=' + encodeURIComponent(error.message));
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