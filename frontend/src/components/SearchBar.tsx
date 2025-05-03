interface SearchBarProps {
    value: string;
    onChange: (value: string) => void;
    onSearch: () => void;
}

const SearchBar = ({value, onChange, onSearch} : SearchBarProps) => {
    return (
        <div className="flex">
            <input
                type="text"
                value={value}
                onChange={e => onChange(e.target.value)}
                className="border p-2 rounded-l w-full"
                placeholder="종목이나 심볼 입력"
            />
            <button
                onClick={onSearch}
                className="bg-blue-500 text-white px-4 rounded-r"
            >
                검색
            </button>
        </div>
    );
};

export default SearchBar;