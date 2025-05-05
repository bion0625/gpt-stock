import { useState } from "react";
import { searchStocks } from "../services/api";
import SimpleStockCard from "../components/SimpleStockCard";
import SearchBar from "../components/SearchBar";

interface Stock {
    symbol: string;
    name: string;
    market: string;
    is_in_portfolio: boolean;
}

const StocksSearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Stock[]>([]);

    const handleSearch = async () => {
        try {
            const data = await searchStocks(query);
            setResults(data);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="px-4">
            <h1 className="text-2xl font-bold mb-4">종목 검색</h1>
            <SearchBar value={query} onChange={setQuery} onSearch={handleSearch}/>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                {results.map(stock => 
                    <SimpleStockCard key={stock.symbol} symbol={stock.symbol} name={stock.name} market={stock.market} is_in_portfolio={stock.is_in_portfolio}/>
                )}
            </div>
        </div>
    )
}

export default StocksSearchPage;