import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"

const NavBar = () => {
    const { isLoggedIn, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    }

    return (
        <nav className="h-16 bg-gray-800 text-white flex items-center justify-between px-8">
          {/* 왼쪽: 메인 메뉴 */}
          <div className="flex items-center space-x-6">
            <Link to="/" className="hover:bg-gray-700 px-2 px-1 rounded">홈</Link>
            {isLoggedIn && (
                <>
                    <Link to="/stocks" className="hover:bg-gray-700 px-2 px-1 rounded">종목 리스트</Link>
                    <Link to="/search" className="hover:bg-gray-700 px-2 px-1 rounded">종목 검색</Link>
                    <Link to="/portfolio" className="hover:bg-gray-700 px-2 px-1 rounded">포트폴리오</Link>
                </>
            )}
          </div>

          {/* 오른쪽: 계정 관련 */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
                <button onClick={handleLogout} className="hover:bg-gray-700 px-2 px-1 rounded">로그아웃</button>
            ) : (
                <>
                    <Link to="/login" className="hover:bg-gray-700 px-2 px-1 rounded">로그인</Link>
                    <Link to="/register" className="hover:bg-gray-700 px-2 px-1 rounded">회원가입</Link>
                </>
            )}
          </div>
        </nav>
    )
}

export default NavBar;