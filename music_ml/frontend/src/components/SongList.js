import React from "react";
import { Card, CardContent, Typography, CardActionArea, Box } from "@mui/material";

const SongList = ({ songs = [], onSongSelect }) => {
  return (
    <Box sx={{ 
      display: 'flex',
      flexDirection: 'column',
      gap: 1  // Reduced gap between cards
    }}>
      {songs.map((song) => (
        <Card
          key={song.spotify_track_id}
          sx={{
            backgroundColor: '#34353b',
            color: 'white',
            '&:hover': {
              backgroundColor: '#404040',
            }
          }}
        >
          <CardActionArea onClick={() => onSongSelect(song)}>
            <CardContent sx={{ py: 1 }}>  {/* Reduced padding */}
              <Typography 
                variant="body1" 
                component="div" 
                sx={{ 
                  color: 'white',
                  fontSize: '0.9rem',  // Slightly smaller font
                  fontWeight: 500
                }}
              >
                {song.track_name}
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: '#b3b3b3',
                  fontSize: '0.8rem'  // Smaller font for artist
                }}
              >
                {song.artist.name}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      ))}
    </Box>
  );
};

export default SongList;