import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchStockDetail, fetchStockHistory, fetchStockRecommendation } from "../services/api";
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const StockDetailPage = () => {
    const { symbol } = useParams<{symbol: string}>();

    const [detail, setDetail] = useState<any>(null);
    const [history, setHistory] = useState<any[]>([]);
    const [recommend, setRecommend] = useState<any>(null);

    const [period, setPeriod] = useState("1mo");

    useEffect(() => {
        const loadData = async () => {
            const detailData = await fetchStockDetail(symbol!);
            setDetail(detailData);

            const historyData = await fetchStockHistory(symbol!, period);
            setHistory(historyData.data);

            const recommendData = await fetchStockRecommendation(symbol!);
            setRecommend(recommendData);
        }

        loadData();
    }, [symbol, period]);

    return (
        <div className="bg-green-100 px-4">
            <h1 className="text-3xl text-center">{symbol} 상세</h1>

            <div className="mt-4">
                <h2 className="text-xl">현재 정보</h2>
                <p>날짜: {detail?.date}</p>
                <p>현재가: {detail?.close}</p>
                {/* <p>고가: {detail?.high}</p>
                <p>저가: {detail?.low}</p>
                <p>거래량: {detail?.volume}</p> */}
            </div>

            <div className="flex space-x-2">
                <button onClick={() => setPeriod("7d")} className="p-2 bg-blue-500 text-white rounded">최근 7일</button>
                <button onClick={() => setPeriod("1mo")} className="p-2 bg-blue-500 text-white rounded">1개월</button>
                <button onClick={() => setPeriod("1y")} className="p-2 bg-blue-500 text-white rounded">1년</button>
            </div>
            
            <div className="mt-4">
                <h2 className="text-xl">과거 데이터 (종가 추세선)</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={history}>
                        <CartesianGrid strokeDasharray="3.3" />
                        <XAxis dataKey="date"/>
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="close" stroke="#8884d8" />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-4">
                <h2 className="text-xl">거래량 (막대 차트)</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={history}>
                        <CartesianGrid strokeDasharray="3.3" />
                        <XAxis dataKey="date"/>
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="volume" fill="#82ca9d" />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-4">
                <h2 className="text-xl">추천 전략</h2>
                <p>추천: {recommend?.recommandation}</p>
                <p>이유: {recommend?.reason}</p>
                <div>
                    <h3>세부 정보</h3>
                    <p>현재 가격: {recommend?.details?.current_price}</p>
                    <p>20일 이동평균: {recommend?.details?.moving_average_20}</p>
                    <p>RSI(14): {recommend?.details?.rsi_14}</p>
                </div>
            </div>
        </div>
    );
};

export default StockDetailPage;