import React from "react";
import { Card, CardContent, Typography, CardActionArea, Box } from "@mui/material";

const SongList = ({ songs = [], onSongSelect }) => {
  return (
    <Box sx={{ padding: 2 }}>
      {songs.map((song) => (
        <Card
          key={song.spotify_track_id}
          sx={{
            backgroundColor: '#34353b', // Dark background
            color: 'white', // Light text color
            marginBottom: 2, // Add space between cards
          }}
        >
          <CardActionArea onClick={() => onSongSelect(song)}>
            <CardContent>
              <Typography gutterBottom variant="h6" component="div" sx={{ color: 'white' }}>
                {song.track_name}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ color: '#b3b3b3' }}>
                {song.artist}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      ))}
    </Box>
  );
};

export default SongList;