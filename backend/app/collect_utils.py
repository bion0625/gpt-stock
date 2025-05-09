import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """
    지정한 종목(symbol)의 최근 주가 데이터를 수집한다.

    Args:
        symbol (str): 주식 코드 (예: AAPL, MSFT, 005930.KQ)
        period (str): 기간 (예: "1mo", "3mo", "1y")
        interval (str): 간격 (예: "1d", "1wk", "1mo")
    
    Returns:
        pd.DataFrame: 종가, 시가, 고가, 저가, 거래량 포함 데이터프레임
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    
    if df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    df.reset_index(inplace=True)
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.columns = [["date", "open", "high", "low", "close", "volume"]]
    
    return df

def fetch_stock_history_data(symbols: list[str], period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    여러 종목(symbols)의 최근 주가 데이터를 한 번에 수집한다.

    Args:
        symbols (list[str]): 주식 코드 리스트 (예: ["AAPL", "MSFT", "005930.KQ"])
        period (str): 기간 (예: "1mo", "3mo", "1y")
        interval (str): 간격 (예: "1d", "1wk", "1mo")
    
    Returns:
        pd.DataFrame: 종목별 멀티컬럼 데이터프레임임
    """

    df = yf.download(
        tickers=symbols,
        period=period,
        interval=interval,
        group_by='ticker',
        auto_adjust=True,
        threads=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data found for symbols: {symbols}")
    
    result = {}

    if isinstance(df.columns, pd.MultiIndex):
        # 멀티심볼: 각 심볼별로 분리
        for symbol in symbols:
            if (symbol, 'Open') in df.columns:
                df_symbol = df[symbol].copy()
                df_symbol.reset_index(inplace=True)
                df_symbol = df_symbol[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                df_symbol.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
                result[symbol] = df_symbol
    else:
        # 단일 심볼: 통째로 처리
        df.reset_index(inplace=True)
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        result[symbols[0]] = df
    
    return result

# 테스트 코드
if __name__== "__main__":
    df = fetch_stock_data("AAPL", period="1mo")
    print(df.head())