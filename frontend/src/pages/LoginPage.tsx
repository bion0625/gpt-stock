import { useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post('/token', new URLSearchParams({
                username,
                password
            }));
            login(res.data.access_token);
            navigate('/');
        } catch (err) {
            setError('로그인 실패: 아이디 또는 비밀번호가 틀렸습니다.');
        }
    };

    return (
        <div className="flex items-center justify-center">
            <form className="bg-white p-8 rounded shadow-md w-96" onSubmit={handleLogin}>
                <h2 className="text-2xl font-bold mb-4 text-center">로그인</h2>
                {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
                <input
                    className="w-full p-2 border mb-3 rounded"
                    type="text"
                    placeholder="아이디"
                    value={username}
                    onChange={(e) => setUsername(() => e.target.value)}
                />
                <input
                    className="w-full p-2 border mb-3 rounded"
                    type="password"
                    placeholder="비밀번호"
                    value={password}
                    onChange={e => setPassword(() => e.target.value)}
                />
                <button className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
                    로그인
                </button>
            </form>
        </div>
    )
}

export default LoginPage;