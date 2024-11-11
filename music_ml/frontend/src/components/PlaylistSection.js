import React from 'react';
import { Box, Typography, Grid, Card, CardContent, CardMedia, CardActionArea, Button } from '@mui/material';

const PlaylistSection = ({ playlist, onSongSelect, isAuthenticated }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      gap: 2,
      height: '100%',
      color: '#fff'
    }}>
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center'
      }}>
        <Typography variant="h6" sx={{ color: '#fff' }}>
          Generated Playlist
        </Typography>
        
        <Button
          variant="contained"
          disabled={!playlist || !isAuthenticated}
          sx={{
            backgroundColor: '#1DB954',  // Spotify green
            color: '#fff',
            textTransform: 'none',
            fontSize: '0.9rem',
            fontWeight: 500,
            '&:hover': {
              backgroundColor: '#1ed760'
            },
            '&.Mui-disabled': {
              backgroundColor: 'rgba(29, 185, 84, 0.3)',
              color: 'rgba(255, 255, 255, 0.3)'
            }
          }}
        >
          {isAuthenticated ? 'Export to Spotify' : 'Login to Export'}
        </Button>
      </Box>
      
      <Box sx={{ 
        border: '1px solid #404040',
        borderRadius: 2, 
        padding: 2,
        flexGrow: 1,
        overflowY: 'auto',
        '&::-webkit-scrollbar': {
          width: '8px',
        },
        '&::-webkit-scrollbar-track': {
          background: 'transparent',
        },
        '&::-webkit-scrollbar-thumb': {
          background: '#888',
          borderRadius: '4px',
        },
        '&::-webkit-scrollbar-thumb:hover': {
          background: '#555',
        },
      }}>
        {playlist && playlist.tracks ? (
          <Grid container spacing={1.5}>
            {playlist.tracks.map((song) => (
              <Grid item xs={2.4} key={song.spotify_track_id}>
                <Card 
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    backgroundColor: '#34353b',
                    borderRadius: 1.5,
                    '&:hover': {
                      backgroundColor: '#404040',
                      transform: 'scale(1.02)',
                      transition: 'all 0.2s ease-in-out'
                    }
                  }}
                >
                  <CardActionArea onClick={() => onSongSelect(song)}>
                    <CardMedia
                      component="img"
                      image={song.album_image_url || 'https://via.placeholder.com/300'}
                      alt={song.track_name}
                      sx={{ 
                        aspectRatio: '1',
                        objectFit: 'cover',
                        width: '100%',
                        height: 'auto',
                        borderBottom: '1px solid rgba(255,255,255,0.1)'
                      }}
                    />
                    <CardContent 
                      sx={{ 
                        p: 1,
                        '&:last-child': { pb: 1 },
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 0.25
                      }}
                    >
                      <Typography 
                        variant="body2"
                        component="div"
                        sx={{ 
                          color: '#fff',
                          fontWeight: 600,
                          fontSize: '0.75rem',
                          letterSpacing: '-0.02em',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          lineHeight: 1.2,
                          textAlign: 'left'
                        }}
                      >
                        {song.track_name}
                      </Typography>
                      <Typography 
                        variant="caption"
                        sx={{ 
                          color: 'rgba(255,255,255,0.7)',
                          fontSize: '0.65rem',
                          fontWeight: 400,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          lineHeight: 1.2,
                          textAlign: 'left',
                          letterSpacing: '0.01em'
                        }}
                      >
                        {song.artist.name}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.7)' }}>
            Select a song and click "Generate Playlist" to get started.
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default PlaylistSection; 