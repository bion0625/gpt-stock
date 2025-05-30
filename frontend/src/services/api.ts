import axios from "axios";
import { toast } from "react-toastify";

const api = axios.create({
    baseURL: "http://localhost:8000", // fastAPI 서버 주소
    withCredentials: true
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    response => response,
    async (error) => {
        if (error.response && error.response.status === 401) {
            // 토큰 만료 처리
            localStorage.removeItem('access_token');
            toast.error('세션이 만료되었습니다. 다시 로그인해주세요.');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
)

export default api;

export const getStocks = async () => {
    const res = await api.get('/stocks/list');
    return res.data;
}

export const searchStocks = async (query: string) => {
    const res = await api.get(`/stocks/search?q=${query}`);
    return res.data
}

export const addStock = async (stock: {symbol: string; amount: number}) => {
    const res = await api.post('/portfolio', stock);
    return res.data;
}

export const fetchPortfolio = async () => {
    try {
        const response = await api.get("/portfolio");
        return response.data
    } catch (error) {
        console.error("Error fetching portfolio", error);
        return [];
    }
};

export const fetchStockDetail = async (symbol: string) => {
    const res = await api.get(`stocks/${symbol}`);
    return res.data;
};

export const fetchStockHistory = async (symbol: string, period: string) => {
    const res = await api.get(`stocks/${symbol}/data?period=${period}`);
    return res.data;
};

export const fetchStockRecommendation = async (symbol: string) => {
    const res = await api.get(`recommend/${symbol}`);
    return res.data;
};

export const deleteStock = async (symbol: string) => {
    const res = await api.delete(`/portfolio/${symbol}`);
    return res.data;
};