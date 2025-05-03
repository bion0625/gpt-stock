import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"
import HomePage from "./pages/HomePage"
import PortfolioPage from "./pages/PortfolioPage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import StockDetailPage from "./pages/StockDetailPage"
import StocksPage from "./pages/StocksPage"
import StocksSearchPage from "./pages/StocksSearchPage"
import { ToastContainer } from "react-toastify"

function App() {

  return (
    <Router>
      <nav className="h-16 bg-gray-800 text-white flex items-center justify-between px-8">
        {/* 왼쪽: 메인 메뉴 */}
        <div className="flex items-center space-x-6">
          <Link to="/" className="hover:bg-gray-700 px-2 px-1 rounded">홈</Link>
          <Link to="/stocks" className="hover:bg-gray-700 px-2 px-1 rounded">종목 리스트</Link>
          <Link to="/search" className="hover:bg-gray-700 px-2 px-1 rounded">종목 검색</Link>
          <Link to="/portfolio" className="hover:bg-gray-700 px-2 px-1 rounded">포트폴리오</Link>
        </div>

        {/* 오른쪽: 계정 관련 */}
        <div className="flex items-center space-x-4">
          <Link to="/login" className="hover:bg-gray-700 px-2 px-1 rounded">로그인</Link>
          <Link to="/register" className="hover:bg-gray-700 px-2 px-1 rounded">회원가입</Link>
        </div>
      </nav>
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
  )
}

export default App
