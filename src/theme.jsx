import { createTheme } from "@mui/material";

var primary = "#007958";
var secondary = "#363636";

const theme = createTheme({
  palette: {
    primary: {
      main: primary,
    },
    secondary: {
      main: secondary,
    },
  },
  typography: {
    fontFamily: ["Lato"],
    fontSize: 16,
  },
});

export default theme;