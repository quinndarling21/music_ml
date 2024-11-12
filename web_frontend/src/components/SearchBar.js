import React from "react";
import { TextField, Button, Box } from "@mui/material";

const SearchBar = ({ query, setQuery, onSearch }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        gap: 2,
        alignItems: 'center',
        marginBottom: 2,
      }}
    >
      <TextField
        placeholder="Search for a song"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        fullWidth
        variant="outlined"
        size="small"
        InputProps={{
          sx: {
            color: 'white',
            backgroundColor: 'rgba(255,255,255,0.1)',
            '&:hover': {
              backgroundColor: 'rgba(255,255,255,0.15)',
            },
            '&.Mui-focused': {
              backgroundColor: 'rgba(255,255,255,0.1)',
            },
            '& input::placeholder': {
              color: 'rgba(255,255,255,0.7)',
              opacity: 1,
            },
          }
        }}
        sx={{
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#404040',
            },
            '&:hover fieldset': {
              borderColor: '#666',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#fff',
            },
          },
        }}
      />
      <Button
        variant="contained"
        onClick={onSearch}
        sx={{
          backgroundColor: '#1c1c1c',
          color: 'white',
          minWidth: '100px',
          '&:hover': {
            backgroundColor: '#333333',
          },
        }}
      >
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;