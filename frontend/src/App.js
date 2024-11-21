import React from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import ImageClassifier from './components/ImageClassifier';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <ImageClassifier />
      </Container>
    </ThemeProvider>
  );
}

export default App;