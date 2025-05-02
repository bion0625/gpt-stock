import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchStockDetail, fetchStockHistory, fetchStockRecommendation } from "../services/api";

const StockDetailPage = () => {
    const { symbol } = useParams<{symbol: string}>();

    const [detail, setDetail] = useState<any>(null);
    const [history, setHistory] = useState<any[]>([]);
    const [recommend, setRecommend] = useState<any>(null);

    useEffect(() => {
        const loadData = async () => {
            const detailData = await fetchStockDetail(symbol!);
            setDetail(detailData);

            const historyData = await fetchStockHistory(symbol!);
            setHistory(historyData);

            const recommendData = await fetchStockRecommendation(symbol!);
            setRecommend(recommendData);
        }

        loadData();
    }, [symbol]);

    return (
        <div className="min-h-screen bg-green-100 p-4">
            <h1 className="text-3xl text-center mt-8">{symbol} 상세</h1>

            <div className="mt-4">
                <h2 className="text-xl">현재 정보</h2>
                <p>날짜: {detail?.date}</p>
                <p>종가: {detail?.close}</p>
                <p>고가: {detail?.high}</p>
                <p>저가: {detail?.low}</p>
                <p>거래량: {detail?.volume}</p>
            </div>
            
            <div className="mt-4">
                <h2 className="text-xl">과거 데이터 (차트)</h2>
                {/* Recharts 같은 라이브러리로 history 데이터 차트 시각화 */}
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