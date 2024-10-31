import React, { useState } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import SongList from "./components/SongList";
import SelectedSong from "./components/SelectedSong";
import { searchSongs } from "./services/searchService";
import { generatePlaylist } from "./services/generatePlaylist";
import { Typography, Box, Button } from "@mui/material";

const App = () => {
  const [query, setQuery] = useState("");
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState(null);
  const [playlist, setPlaylist] = useState([]);

  const handleSearch = async () => {
    try {
      const results = await searchSongs(query);
      setSongs(results.tracks);
    } catch (error) {
      console.error("Error during search:", error);
    }
  };

  const handleSongSelect = (song) => {
    setSelectedSong(song);
  };

  const handleGeneratePlaylist = async () => {
    if (!selectedSong) {
      alert("Please select a song first.");
      return;
    }
    try {
      const result = await generatePlaylist(selectedSong.spotify_track_id);
      setPlaylist(result.playlist);
    } catch (error) {
      console.error("Error generating playlist:", error);
    }
  };

  const handleBackToSearch = () => {
    setPlaylist([]);
    setSelectedSong(null);
  };

  return (
    <div className="App">
      <Typography variant="h4" gutterBottom>
        Playlist Generator
      </Typography>
      <Typography variant="h6" gutterBottom>
        Generate a playlist that matches the vibe of a single song.
      </Typography>

      {/* Display selected song */}
      <SelectedSong song={selectedSong} />

      {/* Metallic Silver Button */}
      <Box sx={{ display: 'flex', justifyContent: 'center', marginY: 3 }}>
        <Button
          variant="contained"
          sx={{
            background: 'linear-gradient(145deg, #b5b5b5, #8c8c8c)', // Metallic gradient
            color: '#fff',
            border: '1px solid #d4d4d4', // Silver border
            borderRadius: '5px',
            paddingX: 4,
            paddingY: 1.5,
            boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.2)',
            textTransform: 'none',
            fontSize: '16px',
            '&:hover': {
              background: 'linear-gradient(145deg, #c2c2c2, #7e7e7e)', // Lighter on hover
              boxShadow: '0px 6px 8px rgba(0, 0, 0, 0.3)',
            },
          }}
          onClick={handleGeneratePlaylist}
        >
          Generate Playlist
        </Button>
      </Box>

      {playlist.length === 0 ? (
        <Box
          sx={{
            border: '1px solid #b3b3b3',  // Thin light border
            borderRadius: 2,              // Rounded corners (optional)
            padding: 2,                   // Space inside the box
            marginTop: 4,                 // Space above the box
          }}
        >
          <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch} />
          <SongList songs={songs} onSongSelect={handleSongSelect} />
        </Box>
      ) : (
        // Display the playlist
        <Box
          sx={{
            border: '1px solid #b3b3b3',  // Thin light border
            borderRadius: 2,              // Rounded corners (optional)
            padding: 2,                   // Space inside the box
            marginTop: 4,                 // Space above the box
          }}
        >
          <Typography variant="h6" gutterBottom>
            Generated Playlist
          </Typography>
          <SongList songs={playlist['tracks']} onSongSelect={handleSongSelect} />
          <Box sx={{ display: 'flex', justifyContent: 'center', marginY: 2 }}>
            <Button
              variant="outlined"
              onClick={handleBackToSearch}
              sx={{
                textTransform: 'none',
              }}
            >
              Back to Search
            </Button>
          </Box>
        </Box>
      )}
    </div>
  );
};

export default App;