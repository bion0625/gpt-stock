import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import HomePage from "./pages/HomePage"
import PortfolioPage from "./pages/PortfolioPage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import StockDetailPage from "./pages/StockDetailPage"
import StocksPage from "./pages/StocksPage"
import StocksSearchPage from "./pages/StocksSearchPage"
import { ToastContainer } from "react-toastify"
import { AuthProvider } from "./context/AuthContext"
import NavBar from "./components/NavBar"

function App() {

  return (
    <AuthProvider>
      <Router>
        <NavBar/>
        <Routes>
          <Route path="/" element={<HomePage/>} />
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/register" element={<RegisterPage/>} />
          <Route path="/portfolio" element={<PortfolioPage/>} />
          <Route path="/stocks" element={<StocksPage/>} />
          <Route path="/search" element={<StocksSearchPage/>} />
          <Route path="/stocks/:symbol" element={<StockDetailPage/>} />
        </Routes>
        <ToastContainer/>
      </Router>
    </AuthProvider>
  )
}

export default App
