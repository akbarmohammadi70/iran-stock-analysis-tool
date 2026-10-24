import math
import pytse_client as tse

def get_stock_info(symbol: str) -> dict:
    """
    Return stock information from TSETMC using pytse-client.

    Args:
        symbol: Stock symbol, for example "فولاد".

    Returns:
        A dictionary containing stock prices, volume, market cap,
        and the latest available update timestamp.

    Raises:
        ValueError: If the symbol is empty or invalid.
        RuntimeError: If stock data cannot be retrieved or is incomplete.
    """
    # Validate the input symbol.
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("The stock symbol must be a non-empty string.")

    symbol = symbol.strip()

    # Initialize the ticker and retrieve its data.
    try:
        ticker = tse.Ticker(symbol)
        last_price_raw = ticker.last_price
        yesterday_price_raw = ticker.yesterday_price
        volume_raw = ticker.volume
        last_date = ticker.last_date
        market_cap_raw = ticker.market_cap
        name = ticker.title

    except ValueError as exc:
        raise ValueError(
            f"Stock symbol '{symbol}' was not found or is invalid."
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            f"Could not retrieve data for stock '{symbol}'."
        ) from exc

    # Validate the retrieved price data.
    if last_price_raw is None:
        raise RuntimeError(f"No last price is available for '{symbol}'.")

    last_price = float(last_price_raw) / 10

    if not math.isfinite(last_price):
        raise RuntimeError(f"Invalid last price returned for '{symbol}'.")

    # Calculate the percentage change when yesterday's price is available.
    change_percent = None

    if yesterday_price_raw is not None:
        yesterday_price = float(yesterday_price_raw) / 10

        if math.isfinite(yesterday_price) and yesterday_price != 0:
            change_percent = round(
                (last_price - yesterday_price) / yesterday_price * 100,
                2,
            )

    # Convert market capitalization from rials to tomans.
    market_cap = None

    if market_cap_raw is not None:
        market_cap_value = float(market_cap_raw) / 10

        if math.isfinite(market_cap_value):
            market_cap = market_cap_value

    # Normalize the last update timestamp.
    last_update = last_date.isoformat() if last_date else None

    return {
        "symbol": symbol,
        "name": name,
        "last_price": last_price,
        "price_change_percent": change_percent,
        "volume": int(volume_raw) if volume_raw is not None else None,
        "market_cap": market_cap,
        "last_update": last_update,
    }
