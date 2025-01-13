import './App.css';
import { ThemeProvider } from "@mui/material";
import theme from "./theme";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Dashboard />
    </ThemeProvider>
  );
}

export default App;
