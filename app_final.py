# ---------------------------------------------------------
# This script was collaboratively developed by our group.
# We used OpenAI's ChatGPT to assist with specific coding tasks, including:
#
# CoinGecko API Research
# - Identifying the appropriate API endpoints for OHLC, market data, and historical prices
# - Understanding required parameters and structuring API responses into usable pandas DataFrames
#
# Tab 1: Candlestick Charts (OHLC)
# - Using OHLC data to build candlestick charts with Plotly Graph Objects in Streamlit
# - Formatting date ranges and customizing the chart layout
#
# Tab 2: Bubble Chart (Market Cap vs Volume)
# - Choosing appropriate variables for x, y, size, and color
# - Adjusting axis scaling (linear) and bubble size logic
# - Mapping distinct colors to selected coins and formatting hover text
#
# Tab 3: Volume Distribution
# - Calculating the volume percentage share among top coins
# - Customizing bar colors based on selected coins for visual emphasis
#
# ChatGPT provided code suggestions and critiques, which we reviewed and integrated as a group.
# All final decisions and implementations reflect our understanding and collaborative effort.
# ---------------------------------------------------------

from dotenv import load_dotenv
import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the API key
load_dotenv()
api_key = os.getenv("COINGECKO_API_KEY")
headers = {"x-cg-demo-api-key": api_key}

# Fetch OHLC data (Open, High, Low, Close)
def get_ohlc_data(coin_id, days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd", 
        "days": days
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        df = pd.DataFrame(response.json(), columns=["timestamp", "open", "high", "low", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    return pd.DataFrame()

# Get the top cryptocurrency coins (default value is 5)
def get_top_coins(n=5):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

# Find the historical market price for a given coin (default value is 30 days)
def get_market_chart(coin_id, days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    return pd.DataFrame()

# Configure dashboard layout
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Crypto Market Dashboard")

# Display the top five cryptocurrencies in the sidebar, showing current price and 24-hour price change
df_top5 = get_top_coins(5)
if not df_top5.empty:
    st.sidebar.header("Top Five Cryptocurrencies Overview")
    st.sidebar.markdown("View the current price and 24-hour price change for the top five cryptocurrencies by market cap.")
    for _, row in df_top5.iterrows():
        st.sidebar.metric(
            label=f"{row['name']} ({row['symbol'].upper()})",
            value=f"${row['current_price']:,.2f}",
            delta=f"{row['price_change_percentage_24h']:.2f}%"
        )
    st.sidebar.markdown("---")

# Display a filter on the sidebar that allows user choose up to five cryptocurrencies to analyze
st.sidebar.title("Coin Filters")
st.sidebar.markdown("Select one or more coins to visualize their market trends, trading volume, etc.")
coin_choice = st.sidebar.multiselect(
    "Select Coin(s) to Display", 
    options=df_top5["id"].tolist(), 
    default=df_top5["id"].tolist()[0]
)

# Create a multi-tab dashboard to show each individual data visualization separately
tab1, tab2, tab3 = st.tabs(["Price Overview", "Market Comparison", "Volume Analysis"])

# Tab 1 - Display interactive candlestick charts for selected coins
with tab1:
    st.subheader("Price Movement (Candlestick Chart)")

    if coin_choice:
        # Add dropdown to let user to select time range for historical price data
        days = st.selectbox("Select number of days for OHLC data", [1, 7, 14, 30, 90, 180, 365], index=3)

        for c in coin_choice:
            # Fetch the OHLC data for the selected coin and data range
            df_ohlc = get_ohlc_data(c, days)
            if not df_ohlc.empty:
                # Create a candlestick chart using Plotly Graph Objects
                st.subheader(f"{c.capitalize()} Price Trend (Last {days} Days)")
                fig = go.Figure(go.Candlestick(
                    x=df_ohlc.index,
                    open=df_ohlc["open"],
                    high=df_ohlc["high"],
                    low=df_ohlc["low"],
                    close=df_ohlc["close"]
                ))

                # Update layout to label axes and remove rangeslider
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    xaxis_rangeslider_visible=False
                    )
                st.plotly_chart(fig, use_container_width=True)
    else:
        # Message shown if no coin is selected
        st.info("Please select at least one coin to see candlestick chart.")

# Tab 2 - Display a bubble chart comparing market capitalization and current price, with the bubble size as trading volume
with tab2:
    st.subheader("Market Cap and Current Price Comparison (Bubble Size = Trading Volume)")

    # Filter top five coins based on user selection
    df_bubbles = df_top5[df_top5["id"].isin(coin_choice)].copy()
    st.caption("For better comparison, select multiple coins from the filter.")

    if not df_bubbles.empty:
        # Assign distinct colors to each selected coin
        custom_colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
        coin_ids = df_bubbles["id"].tolist()
        colors = {coin: custom_colors[i % len(custom_colors)] for i, coin in enumerate(coin_ids)}

        # Format hover text for each coin
        hover_text = df_bubbles.apply(
            lambda row: f"<b>{row['name']}</b><br>"
                        f"Current Price: ${row['current_price']:,.2f}<br>"
                        f"Market Cap: ${row['market_cap']:,.0f}<br>"
                        f"Trading Volume in Past 24 Hours (USD): ${row['total_volume']:,.0f}<br>"
                        f"Price Change Over Last 24 Hours: {row['price_change_percentage_24h']:.2f}%",
            axis=1
        )

        # Create a scatter plot, where x = market cap, y = current price, and bubble size = trade volume
        fig = go.Figure(go.Scatter(
            x=df_bubbles["market_cap"],
            y=df_bubbles["current_price"],
            mode='markers+text',
            text=df_bubbles["symbol"].str.upper(),
            textposition="middle center",
            textfont=dict(color="white", size=11),
            marker=dict(
                size=df_bubbles["total_volume"],
                sizemode='area',
                sizeref=2.*max(df_bubbles["total_volume"])/(100**2),
                sizemin=5,
                color=[colors[coin] for coin in df_bubbles["id"]],
                showscale=False
            ),
            hovertext=hover_text,
            hoverinfo="text"
        ))

        # Update layout with a title and formatted axes
        fig.update_layout(
            title="Market Cap vs Current Price (Bubble Size = Trading Volume)",
            xaxis=dict(title="Market Cap (USD)", type="linear", tickformat="$~s"),
            yaxis=dict(title="Current Price (USD)", type="linear", tickformat="$~s"),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Message shown if no coin is selected
        st.info("Please select at least one coin to view bubble chart.")

# Tab 3 - Display a bar chart for trading volume distribution among top 5 coins
with tab3:
    # Calculate the volume percentage for each coin and sort in descending order
    df_top5["percent"] = (df_top5["total_volume"] / df_top5["total_volume"].sum()) * 100
    df_top5 = df_top5.sort_values(by="percent", ascending=False)

    st.subheader("Top Five Cryptocurrencies by Trading Volume Share")
    st.caption("The highlighted color in the bar chart indicates the coin(s) selected from the sidebar filter.")

    if not df_top5.empty:
        # Create a bar chart to visualize the volume share of each coin
        bar_fig = go.Figure(go.Bar(
            x=df_top5["name"], 
            y=df_top5["percent"],
            text=df_top5["percent"].apply(lambda x: f"{x:.2f}%"),
            textposition='auto',
            marker_color=["steelblue" if c in coin_choice else "lightgray" for c in df_top5["id"]],
            hovertemplate='Cryptocurrency: %{x}<br>Volume Share: %{text}<extra></extra>'
            ))
        
        # Update layout with titles and y-axis formatting
        bar_fig.update_layout(
            title="Trading Volume Share (Top Five Cryptocurrencies)",
            xaxis_title="Cryptocurrency",
            yaxis_title="Volume Share (%)",
            yaxis=dict(tickformat=".0f")
        )
        st.plotly_chart(bar_fig, use_container_width=True)