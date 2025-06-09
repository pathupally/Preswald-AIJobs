"""
World Stocks Explorer - Interactive Analysis Dashboard

This Preswald application provides real-time analysis of global stock market data,
featuring interactive visualizations and dynamic filtering capabilities.
"""

from typing import List, Optional
from datetime import datetime, timedelta

from preswald import connect, get_df, query, table, text, plotly, slider, selectbox, get_workflow
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Connect to Preswald
try:
    connect()
except Exception as e:
    text("⚠️ Error connecting to Preswald. Please check your configuration.")
    raise

workflow = get_workflow()

@workflow.atom
def load_data():
    try:
        df_raw = get_df("World-Stock-Prices-Dataset.csv")
        df_raw['date'] = pd.to_datetime(df_raw['date'])
        df_clean = df_raw.dropna()
        required_columns = ['date', 'exchange', 'symbol', 'close']
        missing_cols = [col for col in required_columns if col not in df_clean.columns]
        if missing_cols:
            text(f"⚠️ Error: Missing required columns: {missing_cols}")
            return None
        return df_clean
    except Exception as e:
        text(f"⚠️ Error loading data: {str(e)}")
        return None

@workflow.atom
def title_text():
    return text("# 🌍 World Stocks Explorer")

@workflow.atom
def subtitle_text():
    return text("Analyze global stock market movements with interactive visualizations")

@workflow.atom
def rolling_window_slider():
    return slider(
        "Rolling Window (days)",
        min_value=5,
        max_value=60,
        value=30,
        help="Adjust the window size for moving averages"
    )

@workflow.atom
def exchange_selectbox(df=load_data()):
    if df is None:
        return selectbox("Exchange", options=["All"], help="No data loaded")
    return selectbox(
        "Exchange",
        options=["All"] + sorted(df['exchange'].unique().tolist()),
        help="Select a specific exchange or view all"
    )

@workflow.atom
def filtered_data(df=load_data(), rolling_window=rolling_window_slider(), exchange=exchange_selectbox()):
    if df is None:
        return None
    if exchange != "All":
        filtered_df = df[df['exchange'] == exchange].copy()
    else:
        filtered_df = df.copy()
    one_year_ago = datetime.now() - timedelta(days=365)
    filtered_df = filtered_df[filtered_df['date'] >= one_year_ago].copy()
    filtered_df = filtered_df.sort_values(['exchange', 'symbol', 'date'])
    filtered_df['daily_change'] = filtered_df.groupby(['exchange', 'symbol'])['close'].pct_change() * 100
    filtered_df['rolling_avg'] = filtered_df.groupby(['exchange', 'symbol'])['close'].rolling(window=rolling_window, min_periods=1).mean().reset_index(0, drop=True)
    filtered_df['rolling_std'] = filtered_df.groupby(['exchange', 'symbol'])['close'].rolling(window=rolling_window, min_periods=1).std().reset_index(0, drop=True)
    filtered_df['upper_band'] = filtered_df['rolling_avg'] + (2 * filtered_df['rolling_std'])
    filtered_df['lower_band'] = filtered_df['rolling_avg'] - (2 * filtered_df['rolling_std'])
    return filtered_df

@workflow.atom
def analysis_period_text(rolling_window=rolling_window_slider()):
    return text(f"### 📊 Analysis Period\nLast 365 days with {rolling_window}-day rolling window")

@workflow.atom
def market_overview_text(filtered_df=filtered_data(), exchange=exchange_selectbox()):
    if filtered_df is None:
        return text("No data available.")
    return text(f"### 📈 Market Overview\nAnalyzing {len(filtered_df['symbol'].unique())} stocks" + (f" on {exchange}" if exchange != "All" else " across all exchanges"))

@workflow.atom
def latest_update_text(filtered_df=filtered_data()):
    if filtered_df is None or filtered_df.empty:
        return text("No recent data.")
    return text(f"### 📅 Latest Update\nData as of {filtered_df['date'].max().strftime('%Y-%m-%d')}")

@workflow.atom
def swings_table(filtered_df=filtered_data()):
    if filtered_df is None or filtered_df.empty:
        return table(pd.DataFrame(), title="No swings data available")
    swings_df = (filtered_df
                .nlargest(10, 'daily_change', key=abs)
                [['date', 'exchange', 'symbol', 'close', 'daily_change']]
                .round(2))
    return table(swings_df, title="Top 10 Largest Daily Price Movements")

@workflow.atom
def price_analysis_text():
    return text("### 📈 Price Analysis")

@workflow.atom
def price_chart(filtered_df=filtered_data(), exchange=exchange_selectbox()):
    if filtered_df is None or filtered_df.empty:
        return plotly(go.Figure())
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['rolling_avg'],
        name='Rolling Average',
        line=dict(color='#2563eb', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['upper_band'],
        name='Upper Band',
        line=dict(color='rgba(37, 99, 235, 0.2)', width=1),
        fill=None
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['lower_band'],
        name='Lower Band',
        line=dict(color='rgba(37, 99, 235, 0.2)', width=1),
        fill='tonexty'
    ))
    fig.update_layout(
        title=f"{exchange} Price Analysis with Bollinger Bands" if exchange != "All" else "Global Price Analysis with Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        showlegend=True,
        hovermode='x unified'
    )
    return plotly(fig)

@workflow.atom
def main():
    title_text()
    subtitle_text()
    rolling_window_slider()
    exchange_selectbox()
    analysis_period_text()
    market_overview_text()
    latest_update_text()
    swings_table()
    price_analysis_text()
    price_chart()

if __name__ == "__main__":
    main()
    workflow.execute() 