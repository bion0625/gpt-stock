import { useEffect, useState } from "react";
import { getStocks } from "../services/api";
import SimpleStockCard from "../components/SimpleStockCard";

interface Stock {
    symbol: string;
    name: string;
    market: string;
}

const StocksPage = () => {
    const [stocks, setStocks] = useState<Stock[]>([]);

    useEffect(() => {
        getStocks().then(setStocks).catch(err => console.error(err));
    }, []);

    return (
        <div className="px-4">
            <h1 className="text-2xl font-bold mb-4">종목 리스트</h1>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {stocks.map(stock => 
                    <SimpleStockCard key={stock.symbol} symbol={stock.symbol} name={stock.name} market={stock.market}/>
                )}
            </div>
        </div>
    )
}

export default StocksPage;