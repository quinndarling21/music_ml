import React from "react";
import { List, ListItem, ListItemText } from "@mui/material";

const SongList = ({ songs = [], onSongSelect }) => {
  console.log(songs)
  return (
    <List className="results-list">
      {songs.map((song) => (
        <ListItem button key={song.spotify_track_id} onClick={() => onSongSelect(song)}>
          <ListItemText primary={song.track_name} secondary={song.artist} />
        </ListItem>
      ))}
    </List>
  );
};

export default SongList;