import { useNavigate } from "react-router-dom";

interface SimpleStockCardProps {
    symbol: string;
    name: string;
    market: string;
}

const SimpleStockCard = ({symbol, name, market} : SimpleStockCardProps) => {
    const navigate = useNavigate();

    const MarketMap: Record<string, string> = {
        KOSPI: "KS",
        KOSDAQ: "KQ"
    };

    return (
        <div className="bg-white px-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-100"
            onClick={() => navigate(`/stocks/${symbol}.${MarketMap[market]}`)}>
            <h2>{name} ({symbol})</h2>
            <p>{market}</p>
        </div>
    );
};

export default SimpleStockCard;