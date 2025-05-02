import { useState } from "react";

const AddStockForm = ({onAdd} : {onAdd: (symbol: string, amount: number) => void}) => {
    const [symbol, setSymbol] = useState("");
    const [amount, setAmount] = useState(0);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!symbol || amount <= 0) return;
        onAdd(symbol, amount);
        setSymbol("");
        setAmount(0);
    }

    return (
        <form onSubmit={handleSubmit} className="flex gap-2">
            <input
                value={symbol}
                onChange={e => setSymbol(() => e.target.value)}
                placeholder="Symbol"
                className="border p-2 rounded"
            />
            <input
                value={amount}
                onChange={e => setAmount(() => Number(e.target.value))}
                placeholder="Amount"
                className="border p-2 rounded"
            />
            <button type="submit" className="bg-green-500 text-white px-4 rounded">
                Add
            </button>
        </form>
    );
}

export default AddStockForm;