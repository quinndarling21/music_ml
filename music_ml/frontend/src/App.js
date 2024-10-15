import React, { useState } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import SongList from "./components/SongList";
import SelectedSong from "./components/SelectedSong";
import { searchSongs } from "./services/searchService";
import { Typography } from "@mui/material";

const App = () => {
  const [query, setQuery] = useState("");
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState(null);

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

  return (
    <div className="App">
      <Typography variant="h4" gutterBottom>
        Song Search
      </Typography>
      <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch} />
      <SongList songs={songs} onSongSelect={handleSongSelect} />
      <SelectedSong song={selectedSong} />
    </div>
  );
};

export default App;
