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
            {isLoggedIn ? (
                <>
                    <Link to="/stocks" className="hover:bg-gray-700 px-2 px-1 rounded">List</Link>
                    <Link to="/search" className="hover:bg-gray-700 px-2 px-1 rounded">Search</Link>
                    <Link to="/portfolio" className="hover:bg-gray-700 px-2 px-1 rounded">Portfolio</Link>
                </>
            ) : <Link to="/" className="hover:bg-gray-700 px-2 px-1 rounded">Home</Link>}
          </div>

          {/* 오른쪽: 계정 관련 */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
                <button onClick={handleLogout} className="hover:bg-gray-700 px-2 px-1 rounded">Logout</button>
            ) : (
                <>
                    <Link to="/login" className="hover:bg-gray-700 px-2 px-1 rounded">Login</Link>
                    <Link to="/register" className="hover:bg-gray-700 px-2 px-1 rounded">Join</Link>
                </>
            )}
          </div>
        </nav>
    )
}

export default NavBar;