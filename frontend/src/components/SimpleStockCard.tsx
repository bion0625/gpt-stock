import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { addStock, deleteStock } from "../services/api";
import { toast } from "react-toastify";

interface SimpleStockCardProps {
    symbol: string;
    name: string;
    market: string;
    is_in_portfolio: boolean;
}

const SimpleStockCard = ({symbol, name, market, is_in_portfolio} : SimpleStockCardProps) => {
    const navigate = useNavigate();

    const [isInPortfolio, setIsInPortfolio] = useState(is_in_portfolio);
    const [isProcessing, setIsProcessing] = useState(false);
    const [amount, setAmount] = useState(0);

    const handleAdd = async (symbolWithMarket: string) => {

        setIsProcessing(true);

        if (amount <= 0) {
            toast.error('추가할 수량을 입력하세요.');
            return;
        }
        
        try {
            await addStock({symbol: symbolWithMarket, amount});
            toast.success('포트폴리오에 추가되었습니다!');
            setIsInPortfolio(true);
        } catch (err: any) {
            toast.error('추가중 오류가 발생했습니다.');
        } finally {
            setIsProcessing(false);
        }
    };

    const handleRemove = async (symbolWithMarket: string) => {
        setIsProcessing(true);
        try {
            await deleteStock(symbolWithMarket);
            toast.success('포트폴리오에서 제거되었습니다!');
            setIsInPortfolio(false);
        } catch(err) {
            toast.error('제거중 오류가 발생했습니다.');
        } finally {
            setIsProcessing(false);
        }
    }

    const MarketMap: Record<string, string> = {
        KOSPI: "KS",
        KOSDAQ: "KQ"
    };

    return (
        <div className="bg-white px-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-100"
            onClick={() => navigate(`/stocks/${symbol}.${MarketMap[market]}`)}>
            <h2>{name} ({symbol})</h2>
            <p>{market}</p>
            <div className="mt-2">
                <input
                    type="number"
                    min={1}
                    value={amount}
                    onClick={e => e.stopPropagation()}
                    onChange={e => setAmount(() => Number(e.target.value))}
                    className="border p-1 rounded w-20 mr-2"
                    placeholder="수량"
                />
                {isInPortfolio ? (
                    <button
                        onClick={e => {
                            e.stopPropagation();
                            handleRemove(`${symbol}`)
                        }}
                        className="mt-2 bg-red-500 text-white px-2 py-1 rounded"
                    >
                        {isProcessing ? '제거 중...' : '포트폴리오 제거'}
                    </button>
                ) : (
                    <button
                        onClick={e => {
                            e.stopPropagation();
                            handleAdd(`${symbol}`)
                        }}
                        className="mt-2 bg-green-500 text-white px-2 py-1 rounded"
                    >
                        {isProcessing ? '추가 중...' : '포트폴리오 추가'}
                    </button>
                )}
            </div>
        </div>
    );
};

export default SimpleStockCard;