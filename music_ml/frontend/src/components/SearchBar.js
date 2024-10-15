import React from "react";
import { TextField, Button, Box } from "@mui/material";

const SearchBar = ({ query, setQuery, onSearch }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        gap: 2, // Adds space between the input and button
        alignItems: 'center',
        marginBottom: 2, // Adds space below the search bar
      }}
    >
      <TextField
        label="Search for a song"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        fullWidth
        variant="outlined"
        InputLabelProps={{
          style: { color: '#b3b3b3' }, // Light gray label color
        }}
        InputProps={{
          style: { color: 'white' }, // White text input color
        }}
        sx={{
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#b3b3b3', // Light gray border
            },
            '&:hover fieldset': {
              borderColor: 'white', // White border on hover
            },
            '&.Mui-focused fieldset': {
              borderColor: 'white', // White border when focused
            },
          },
        }}
      />
      <Button
        variant="contained"
        onClick={onSearch}
        sx={{
          backgroundColor: '#1c1c1c', // Dark button background
          color: 'white', // White text
          '&:hover': {
            backgroundColor: '#333333', // Slightly lighter on hover
          },
        }}
      >
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;