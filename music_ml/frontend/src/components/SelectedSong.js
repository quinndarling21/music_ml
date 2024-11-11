import React from "react";
import { Typography, Box, Card, CardMedia, Button } from "@mui/material";

const SelectedSong = ({ song, onGeneratePlaylist }) => {
  if (!song) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center',
        alignItems: 'center',
        padding: 3,
        color: 'rgba(255,255,255,0.7)',
        minHeight: '120px'
      }}>
        <Typography 
          variant="body1"
          sx={{
            fontSize: '0.9rem',
            fontWeight: 500
          }}
        >
          No song selected.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 3,
      padding: 3,
      color: '#fff'
    }}>
      {/* Left side: Album and Song Info */}
      <Box sx={{ 
        display: 'flex',
        alignItems: 'center',
        gap: 3,
        flex: 1,
        minWidth: 0  // Allow text to shrink if needed
      }}>
        {/* Album Image */}
        <Card sx={{ 
          width: 100,
          height: 100,
          flexShrink: 0,
          backgroundColor: 'transparent',
          borderRadius: 1,
          overflow: 'hidden',
          boxShadow: '0 4px 12px rgba(0,0,0,0.4)'
        }}>
          <CardMedia
            component="img"
            image={song.album_image_url || 'https://via.placeholder.com/100'}
            alt={song.track_name}
            sx={{ 
              width: '100%',
              height: '100%',
              objectFit: 'cover'
            }}
          />
        </Card>

        {/* Song Info */}
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 0.75,
          minWidth: 0  // Allow text to shrink
        }}>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 600,
              fontSize: '1.1rem',
              lineHeight: 1.2,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}
          >
            {song.track_name}
          </Typography>
          <Typography 
            variant="subtitle1" 
            sx={{ 
              color: 'rgba(255,255,255,0.7)',
              fontWeight: 400,
              fontSize: '0.9rem',
              lineHeight: 1.2,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}
          >
            {song.artist.name}
          </Typography>
        </Box>
      </Box>

      {/* Generate Button */}
      <Button
        variant="contained"
        onClick={onGeneratePlaylist}
        sx={{
          backgroundColor: '#1DB954',  // Spotify green
          color: '#fff',
          padding: '10px 24px',
          textTransform: 'none',
          fontSize: '16px',
          fontWeight: 500,
          flexShrink: 0,  // Prevent button from shrinking
          '&:hover': {
            backgroundColor: '#1ed760'
          }
        }}
      >
        Generate Playlist
      </Button>
    </Box>
  );
};

export default SelectedSong;