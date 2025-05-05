import { Link, useNavigate } from "react-router-dom";

interface StockCardProps {
    name: string;
    symbol: string;
    amount: number;
    price: number;
}

const StockCard = ({symbol, amount, name, price, onDelete}: StockCardProps & {onDelete: (symbol: string) => void}) => {

    const navigate = useNavigate();

    return (
        <div className="bg-white p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold">{name}</h2>
            <p className="text-lg">symbol: {symbol}</p>
            <p className="text-lg">price: {price}</p>
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