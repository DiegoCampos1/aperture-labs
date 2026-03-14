import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1B3A5C",
    },
    secondary: {
      main: "#1DBF73",
    },
    background: {
      default: "#F5F6FA",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#1B3A5C",
      secondary: "#6B7280",
    },
  },
  typography: {
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    h4: {
      fontWeight: 700,
      color: "#1B3A5C",
    },
    h6: {
      fontWeight: 600,
      color: "#1B3A5C",
    },
    body1: {
      color: "#1B3A5C",
    },
    body2: {
      color: "#6B7280",
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: "#F5F6FA",
        },
      },
    },
  },
});

export default theme;
