import requests
import json
from datetime import datetime

def scrapesharesansarstock(ticker):
    """
    Fetches real-time stock data from NEPSE API for a given ticker.
    Returns a dictionary with stock information.
    """
    try:
        ticker = ticker.upper().strip()
        
        # Try the free NEPSE API first
        api_url = f"https://nepsetty.kokomo.workers.dev/api?symbol={ticker}"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        api_data = response.json()
        
        # Check if we got valid data
        if api_data and 'data' in api_data:
            data = api_data['data']
            
            # Extract the stock information
            result = {
                "ticker": ticker,
                "current_price": data.get('ltp', data.get('lastPrice', 0)),
                "52_week_high": data.get('high52', data.get('52_week_high', 0)),
                "52_week_low": data.get('low52', data.get('52_week_low', 0)),
                "120_days_average": data.get('avg120', data.get('average_120_days', 0)),
                "market_cap": data.get('marketCap', "N/A"),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "open": data.get('open', 0),
                "close": data.get('close', 0),
                "volume": data.get('volume', 0),
                "high": data.get('high', 0),
                "low": data.get('low', 0),
                "change": data.get('change', 0),
                "change_percent": data.get('changePercent', 0)
            }
            return result
        
        # Fallback if API returns empty
        raise Exception(f"No data found for ticker {ticker}")
        
    except requests.exceptions.RequestException as e:
        # If API call fails, try alternative method or return error
        raise Exception(f"Failed to fetch data for {ticker}: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Error parsing stock data for {ticker}: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching stock data for {ticker}: {str(e)}")
