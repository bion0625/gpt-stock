import { useState } from "react";
import api from "../services/api";

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [fullname, setFullname] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/register', {username, password, full_name: fullname});
            setMessage('회원가입 성공! 이제 로그인하세요.')
        } catch (err) {
            setMessage('회원가입 실패: 이미 존재하는 사용자일 수 있습니다.')
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <form className="bg-white p-8 rounded shadow-md w-96" onSubmit={handleRegister}>
                <h2 className="text-2xl font-bold mb-4 text-center"></h2>
                {message && <p className="text-sm mb-2">{message}</p>}
                <input
                    className="w-full p-2 p-2 border mb-3 rounded"
                    type="text"
                    placeholder="아이디"
                    value={username}
                    onChange={e => setUsername(() => e.target.value)}
                />
                <input
                    className="w-full p-2 p-2 border mb-3 rounded"
                    type="text"
                    placeholder="이름"
                    value={fullname}
                    onChange={e => setFullname(() => e.target.value)}
                />
                <input
                    className="w-full p-2 p-2 border mb-3 rounded"
                    type="password"
                    placeholder="비밀번호"
                    value={password}
                    onChange={e => setPassword(() => e.target.value)}
                />
                <button className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600">
                    회원가입
                </button>
            </form>
        </div>
    );
}

export default RegisterPage;