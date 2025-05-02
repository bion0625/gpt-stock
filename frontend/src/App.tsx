import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"
import HomePage from "./pages/HomePage"
import PortfolioPage from "./pages/PortfolioPage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import StockDetailPage from "./pages/StockDetailPage"

function App() {

  return (
    <Router>
      <nav className="p-4 bg-gray-800 text-white flex justify-between">
        <div>
          <Link to="/" className="mr-4">홈</Link>
          <Link to="/login" className="mr-4">로그인</Link>
          <Link to="/register" className="mr-4">회원가입</Link>
          <Link to="/portfolio">포트폴리오</Link>
        </div>
      </nav>
      <Routes>
        <Route path="/login" element={<LoginPage/>} />
        <Route path="/register" element={<RegisterPage/>} />
        <Route path="/" element={<HomePage/>} />
        <Route path="/portfolio" element={<PortfolioPage/>} />
        <Route path="/portfolio/:symbol" element={<StockDetailPage/>} />
      </Routes>
    </Router>
  )
}

export default App
