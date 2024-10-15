import React from "react";
import { Typography, Card, CardContent, CardMedia, Box } from "@mui/material";

const SelectedSong = ({ song }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center', // Centers horizontally
        alignItems: 'center', // Centers vertically
        padding: 2, // Add padding around the card
      }}
    >
      {song ? (
        <Card sx={{ 
          padding: 2,
          backgroundColor: '#654873', // Dark background
          color: 'white'
          }}>
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {song.track_name}
            </Typography>
            <Typography variant="body2">
              {song.artist}
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Typography variant="body1">No song selected.</Typography>
      )}
    </Box>
  );
};

export default SelectedSong;