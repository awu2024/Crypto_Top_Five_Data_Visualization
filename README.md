# Crypto_Top_Five_Data_Visualization
This is a data visualization that uses the CoinGecko API
For our data visualization final project, we chose a cryptocurrency dataset because cryptocurrency has become popular in the financial market and it allows many investment opportunities since cryptocurrency operate continuously 24/7, unlike traditional financial markets. Our project uses real-time cryptocurrency market data to build a dashboard that visualizes prices, market trends, and trading volume distribution. We focused on the top five cryptocurrencies sorted by market capitalization to help our users get a better understanding of the current market in cryptocurrency with clear and informative visualizations.
The data we used in this project is obtained from the CoinGecko API, which provides up-to-date information on various crypto market data, including prices, market capitalization, and trading volume.
Link to CoinGecko API documentation: https://docs.coingecko.com/v3.0.1/reference/introduction
We utilized the following API endpoints from the CoinGecko platform:
OHLC Data Endpoint:
https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc
Purpose: Retrieves Open, High, Low, Close (OHLC) data for selected cryptocurrencies.
Parameters:
- coin_id: The ID of the cryptocurrency (e.g. bitcoin).
- vs_currency: The target currency (e.g. USD).
- days: The time period for the OHLC data.
Market Chart Endpoint:
https://api.coingecko.com/api/v3/coins/markets 
Purpose: Retrieves the top cryptocurrencies by market capitalization.
Parameters:
- vs_currency: The target currency.
- order: Sort order by market cap (e.g., market cap descending).
- per_page: The number of coins to retrieve.
Market Chart Endpoint:
https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart
Purpose: Provides historical market data (prices) for selected cryptocurrencies
Parameters:
- coin_id: The ID of the cryptocurrency.
- vs_currency: The target currency.
- days: The time range for historical data.
