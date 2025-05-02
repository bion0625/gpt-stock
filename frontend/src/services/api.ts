import axios from "axios";

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

export default api;

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
    const res = await api.get(`portfolio/${symbol}`);
    return res.data;
}

export const deleteStock = async (symbol: string) => {
    const res = await api.delete(`/portfolio/${symbol}`);
    return res.data;
}