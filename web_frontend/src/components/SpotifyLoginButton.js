import React, { useState, useEffect } from 'react';
import { Button, Box, Typography } from '@mui/material';
import { authService } from '../services/authService';

const SpotifyLoginButton = ({ isAuthenticated, onLoginSuccess, onLogoutSuccess }) => {
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      fetchUserInfo();
    }
  }, [isAuthenticated]);

  const fetchUserInfo = async () => {
    try {
      const info = await authService.getUserInfo();
      setUserInfo(info);
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  };

  const handleLogin = async () => {
    try {
      const authUrl = await authService.getLoginUrl();
      window.location.href = authUrl;
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      setUserInfo(null);
      if (onLogoutSuccess) onLogoutSuccess();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      {userInfo && (
        <Typography variant="body1">
          Welcome, {userInfo.display_name}
        </Typography>
      )}
      <Button
        variant="contained"
        onClick={isAuthenticated ? handleLogout : handleLogin}
        sx={{
          backgroundColor: '#1DB954', // Spotify green
          '&:hover': {
            backgroundColor: '#1ed760'
          }
        }}
      >
        {isAuthenticated ? 'Logout of Spotify' : 'Login with Spotify'}
      </Button>
    </Box>
  );
};

export default SpotifyLoginButton; 