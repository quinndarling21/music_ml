import React from "react";
import { Typography } from "@mui/material";

const SelectedSong = ({ song }) => {
  return (
    <div className="selected-song">
      {song ? (
        <>
          <Typography variant="h6">Selected Song:</Typography>
          <Typography variant="body1">
            {song.track_name} by {song.artist}
          </Typography>
        </>
      ) : (
        <Typography variant="body1">No song selected.</Typography>
      )}
    </div>
  );
};

export default SelectedSong;