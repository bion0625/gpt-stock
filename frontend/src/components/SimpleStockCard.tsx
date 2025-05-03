import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { addStock } from "../services/api";
import { toast } from "react-toastify";

interface SimpleStockCardProps {
    symbol: string;
    name: string;
    market: string;
}

const SimpleStockCard = ({symbol, name, market} : SimpleStockCardProps) => {
    const navigate = useNavigate();

    const [isAdding, setIsAdding] = useState(false);
    const [add, setAdd] = useState(false);
    const [amount, setAmount] = useState(0);

    const handleAdd = async (symbolWithMarket: string) => {

        if (amount <= 0) {
            toast.error('추가할 수량을 입력하세요.');
            return;
        }

        setIsAdding(true);
        try {
            await addStock({symbol: symbolWithMarket, amount});
            toast.success('포트폴리오에 추가되었습니다!');
            setAdd(true);
        } catch (err: any) {
            if (err.reponse?.status === 409) {
                toast.error('이미 포트폴리오에 추가된 종목입니다.')
            } else {
                toast.error('추가중 오류가 발생했습니다.')
            }
        } finally {
            setIsAdding(false);
        }
    };

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
                <button
                    onClick={e => {
                        e.stopPropagation();
                        handleAdd(`${symbol}.${MarketMap[market]}`)
                    }}
                    className="mt-2 bg-green-500 text-white px-2 py-1 rounded"
                >
                    {add ? '추가됨' : isAdding ? '추가 중...' : '포트폴리오 추가'}
                </button>
            </div>
        </div>
    );
};

export default SimpleStockCard;