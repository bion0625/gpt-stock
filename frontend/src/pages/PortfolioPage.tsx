import { useEffect, useState } from "react"
import StockCard from "../components/StockCard";
import { addStock, deleteStock, fetchPortfolio } from "../services/api";
import AddStockForm from "../components/AddStockForm";

interface Stock {
    symbol: string;
    amount: number;
}

const PortfolioPage = () => {
    const [stocks, setStocks] = useState<Stock[]>([]);
    const [loading, setLoading] = useState(false);

    const getPortfolio = async () => {
        setLoading(true);
        try {
            const data = await fetchPortfolio();
            setStocks(data);
        } catch (err) {
            console.error('Error fetching portfolio', err);
        }
        setLoading(false);
    };

    const handleAdd = async (symbol: string, amount: number) => {
        try {
            await addStock({symbol, amount});
            getPortfolio(); // 추가 후 갱신
        } catch (err) {
            console.error('Error adding stock', err);
        }
    };

    const handleDelete = async (symbol: string) => {
        try {
            await deleteStock(symbol);
            getPortfolio(); // 삭제 후 갱신
        } catch (err) {
            console.error('Error deleting stock', err);
        }
    }

    useEffect(() => {
        getPortfolio();
    }, [])

    return (
        <div className="bg-green-100 px-4">
            <h1 className="text-3xl text-center mt-4">My Portfolio</h1>
            <AddStockForm onAdd={handleAdd}/>
            {loading ? (
                <p className="text-center mt-4">Loading...</p>
            ) : (
                <div className="grid grid-cols-2 gap-4 mt-4">
                    {stocks.map(stock => (
                        <StockCard 
                            key={stock.symbol} 
                            symbol={stock.symbol} 
                            amount={stock.amount}
                            onDelete={handleDelete}
                        />
                    ))}
                </div>
            )}
        </div>
    )
}

export default PortfolioPage