import React from "react";
import { TextField, Button } from "@mui/material";

const SearchBar = ({ query, setQuery, onSearch }) => {
  return (
    <div className="search-bar">
      <TextField
        label="Search for a song"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        fullWidth
      />
      <Button variant="contained" onClick={onSearch}>
        Search
      </Button>
    </div>
  );
};

export default SearchBar;