import { Link, useNavigate } from "react-router-dom";

interface StockCardProps {
    symbol: string;
    amount: number;
}

const StockCard = ({symbol,amount, onDelete}: StockCardProps & {onDelete: (symbol: string) => void}) => {

    const navigate = useNavigate();

    return (
        <div className="bg-white p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold">{symbol}</h2>
            <p className="text-lg">Amount: {amount}</p>
            <div>
                <Link to={`/stocks/${symbol}`}>
                    <button className="pmt-2 p-2 bg-blue-500 text-white rounded-full" onClick={() => navigate(`/stocks/${symbol}`)}>View Details</button>
                </Link>
                <button className="p-2 bg-red-500 text-white rounded-full" onClick={() => onDelete(symbol)}>Delete</button>
            </div>
        </div>
    )
}

export default StockCard