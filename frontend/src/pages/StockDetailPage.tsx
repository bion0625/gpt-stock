import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchStockDetail } from "../services/api";

const StockDetailPage = () => {
    const { symbol } = useParams();
    const [stock, setStock] = useState<any>(null);

    useEffect(() => {
        const getStock = async () => {
            const data = await fetchStockDetail(symbol!)
            setStock(data);
        }
        getStock();
    }, [symbol]);

    if(!stock) return <div>Loading...</div>

    return (
        <div className="min-h-screen bg-yellow-100 p-8">
            <h1 className="text-3xl font-bold mb-4">Details for {stock.symbol}</h1>
            <p className="text-lg">Amount: {stock.amount}</p>
            {/* 추가 정보들: 주가, 평가금액, 수익률 등 */}
        </div>
    );
};

export default StockDetailPage;