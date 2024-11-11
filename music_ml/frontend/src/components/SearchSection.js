import React from 'react';
import { Box } from '@mui/material';
import SearchBar from './SearchBar';
import SongList from './SongList';
import SelectedSong from './SelectedSong';

const SearchSection = ({ query, setQuery, onSearch, songs, onSongSelect, selectedSong }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      gap: 2,
      height: '100%',
      color: '#fff',
      overflow: 'hidden'
    }}>
      <Box sx={{ flexShrink: 0 }}>
        <SearchBar query={query} setQuery={setQuery} onSearch={onSearch} />
      </Box>

      <Box sx={{ 
        border: '1px solid #404040',
        borderRadius: 2, 
        padding: 2,
        flexGrow: 1,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <Box sx={{ 
          overflowY: 'auto',
          flexGrow: 1,
          '&::-webkit-scrollbar': {
            width: '8px',
          },
          '&::-webkit-scrollbar-track': {
            background: 'transparent',
          },
          '&::-webkit-scrollbar-thumb': {
            background: '#888',
            borderRadius: '4px',
          },
          '&::-webkit-scrollbar-thumb:hover': {
            background: '#555',
          },
        }}>
          <SongList songs={songs} onSongSelect={onSongSelect} />
        </Box>
      </Box>
    </Box>
  );
};

export default SearchSection; 