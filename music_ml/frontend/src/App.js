import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import SearchSection from "./components/SearchSection";
import PlaylistSection from "./components/PlaylistSection";
import SelectedSong from "./components/SelectedSong";
import SpotifyCallback from "./components/SpotifyCallback";
import { searchSongs } from "./services/searchService";
import { generatePlaylist } from "./services/generatePlaylist";
import { authService } from "./services/authService";
import { Typography, Box, Button, Container, Grid, Paper } from "@mui/material";

const AppContent = () => {
  const [query, setQuery] = useState("");
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState(null);
  const [playlist, setPlaylist] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const authenticated = await authService.checkAuthStatus();
      setIsAuthenticated(authenticated);
    } catch (error) {
      console.error("Auth check error:", error);
    }
  };

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

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      overflow: 'hidden' // Prevent body scroll
    }}>
      <Header 
        isAuthenticated={isAuthenticated}
        onLogoutSuccess={() => setIsAuthenticated(false)}
      />
      
      <Box sx={{ 
        flex: 1,
        backgroundColor: '#121212',
        overflow: 'hidden' // Prevent content scroll
      }}>
        <Container 
          maxWidth="xl" 
          sx={{ 
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            pt: 4
          }}
        >
          <Typography 
            variant="h6" 
            sx={{ 
              color: 'rgba(255,255,255,0.7)', 
              mb: 4,
              flexShrink: 0 // Prevent title from shrinking
            }}
          >
            Generate a playlist that matches the vibe of a single song.
          </Typography>

          <Box sx={{ 
            display: 'flex', 
            gap: 4,
            flex: 1,
            overflow: 'hidden' // Contain the scrolling areas
          }}>
            {/* Left Sidebar */}
            <Paper
              elevation={6}
              sx={{
                width: '40%',
                backgroundColor: '#282828',
                borderRadius: 2,
                p: 3,
                display: 'flex',
                flexDirection: 'column',
                gap: 3,
                overflow: 'hidden' // Handle overflow within the sidebar
              }}
            >
              {/* Selected Song Section */}
              <Box sx={{ 
                border: '1px solid #404040',
                borderRadius: 2,
                backgroundColor: selectedSong ? '#654873' : 'transparent',
                transition: 'background-color 0.3s ease',  // Smooth transition
                flexShrink: 0, // Prevent shrinking
                overflow: 'hidden' // Contain everything inside
              }}>
                <SelectedSong 
                  song={selectedSong} 
                  onGeneratePlaylist={handleGeneratePlaylist}
                />
              </Box>

              {/* Search Section */}
              <Box sx={{ flex: 1, overflow: 'hidden' }}>
                <SearchSection 
                  query={query}
                  setQuery={setQuery}
                  onSearch={handleSearch}
                  songs={songs}
                  onSongSelect={handleSongSelect}
                  selectedSong={selectedSong}
                />
              </Box>
            </Paper>

            {/* Right Content Area - Generated Playlist */}
            <Box sx={{ 
              flex: 1,
              backgroundColor: '#121212',
              borderRadius: 2,
              p: 2,
              overflow: 'hidden' // Handle overflow within playlist area
            }}>
              <PlaylistSection 
                playlist={playlist}
                onSongSelect={handleSongSelect}
                isAuthenticated={isAuthenticated}
              />
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/callback" element={<SpotifyCallback />} />
        <Route path="/" element={<AppContent />} />
      </Routes>
    </Router>
  );
};

export default App;