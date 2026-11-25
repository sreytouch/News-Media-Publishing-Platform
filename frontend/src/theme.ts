import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1F2937",
      dark: "#111827",
      light: "#4B5563",
    },
    secondary: {
      main: "#B91C1C",
      light: "#EF4444",
      dark: "#7F1D1D",
    },
    background: {
      default: "#F5F4F0",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#14110E",
      secondary: "#57534E",
    },
  },
  shape: {
    borderRadius: 10,
  },
  typography: {
    fontFamily: "\"Inter\", sans-serif",
    h1: { fontFamily: "\"Newsreader\", serif", fontWeight: 700 },
    h2: { fontFamily: "\"Newsreader\", serif", fontWeight: 700 },
    h3: { fontFamily: "\"Newsreader\", serif", fontWeight: 700 },
    h4: { fontFamily: "\"Newsreader\", serif", fontWeight: 600 },
    h5: { fontFamily: "\"Newsreader\", serif", fontWeight: 600 },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
        },
      },
    },
  },
});
