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

Market Capitalization Endpoint:
https://api.coingecko.com/api/v3/coins/markets 

Purpose: Retrieves the top cryptocurrencies by market capitalization.

Parameters:
- vs_currency: The target currency.
- order: Sort order by market cap (e.g., market cap descending).
- per_page: The number of coins to retrieve.
- page: Specifies which page to retrieve.

Market Chart Endpoint:
https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart

Purpose: Provides historical market data (prices) for selected cryptocurrencies

Parameters:
- coin_id: The ID of the cryptocurrency.
- vs_currency: The target currency.
- days: The time range for historical data.

## Acknowledgments
This project was collaboratively developed by our group.

We used OpenAI's ChatGPT to assist with specific coding tasks, including:

### CoinGecko API Research
- Identifying the appropriate API endpoints for OHLC, market data, and historical prices.
- Understanding required parameters and structuring API responses into usable pandas DataFrames.

### Tab 1: Price Overview
- Using OHLC data to build candlestick charts with Plotly Graph Objects in Streamlit.
- Formatting date ranges and customizing the chart layout.

### Tab 2: Market Comparison
- Choosing appropriate variables for x, y, size, and color.
- Adjusting axis scaling (linear) and bubble size logic.
- Mapping distinct colors to selected coins and formatting hover text.

### Tab 3: Volume Analysis
- Calculating the volume percentage share among top coins.
- Customizing bar colors based on selected coins for visual emphasis.

ChatGPT provided code suggestions and critiques, which we reviewed and integrated as a group. All final decisions and implementations reflect our understanding and collaborative effort.
