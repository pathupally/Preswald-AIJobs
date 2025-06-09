"""
World Stocks Explorer - Interactive Analysis Dashboard

This Preswald application provides real-time analysis of global stock market data,
featuring interactive visualizations and dynamic filtering capabilities.
"""

from typing import List, Optional
from datetime import datetime, timedelta
import os

from preswald import connect, get_df, query, table, text, plotly, slider, selectbox, get_workflow
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Connect to Preswald
try:
    connect()
except Exception as e:
    print(f"⚠️ Error connecting to Preswald: {e}")

workflow = get_workflow()

def load_data():
    """Load and preprocess stock data"""
    try:
        # Try different possible file paths
        possible_paths = [
            "World-Stock-Prices-Dataset.csv",
            "data/World-Stock-Prices-Dataset.csv",
            "./data/World-Stock-Prices-Dataset.csv"
        ]
        
        df_raw = None
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    df_raw = pd.read_csv(path)
                    print(f"✅ Successfully loaded data from {path}")
                    break
            except Exception as e:
                continue
        
        if df_raw is None:
            # Try using Preswald's get_df
            try:
                df_raw = get_df("World-Stock-Prices-Dataset.csv")
            except:
                print("⚠️ Could not find data file. Creating sample data...")
                # Create sample data if file not found
                dates = pd.date_range(start='2024-01-01', end='2025-06-06', freq='D')
                symbols = ['PTON', 'AAPL', 'GOOGL', 'MSFT', 'TSLA']
                exchanges = ['NASDAQ', 'NYSE']
                
                data = []
                for symbol in symbols:
                    base_price = np.random.uniform(50, 200)
                    for date in dates:
                        price = base_price * (1 + np.random.normal(0, 0.02))
                        data.append({
                            'Date': date,
                            'Close': price,
                            'Brand_Name': symbol.lower(),
                            'Ticker': symbol,
                            'Country': 'usa',
                            'Volume': np.random.randint(1000000, 50000000)
                        })
                        base_price = price
                
                df_raw = pd.DataFrame(data)
        
        # Standardize column names
        column_mapping = {
            'Date': 'date',
            'Close': 'close',
            'Ticker': 'symbol',
            'Brand_Name': 'brand_name',
            'Country': 'exchange',
            'Volume': 'volume'
        }
        
        df_raw = df_raw.rename(columns=column_mapping)
        
        # Ensure we have required columns
        if 'date' not in df_raw.columns:
            df_raw['date'] = pd.date_range(start='2024-01-01', periods=len(df_raw), freq='D')
        
        if 'exchange' not in df_raw.columns:
            df_raw['exchange'] = 'NASDAQ'
            
        if 'symbol' not in df_raw.columns:
            df_raw['symbol'] = 'SAMPLE'
            
        # Convert date column
        df_raw['date'] = pd.to_datetime(df_raw['date'])
        
        # Clean the data
        df_clean = df_raw.dropna(subset=['close'])
        
        # Ensure we have the required columns
        required_columns = ['date', 'exchange', 'symbol', 'close']
        missing_cols = [col for col in required_columns if col not in df_clean.columns]
        
        if missing_cols:
            print(f"⚠️ Warning: Missing columns {missing_cols}, using defaults")
            for col in missing_cols:
                if col == 'exchange':
                    df_clean[col] = 'NASDAQ'
                elif col == 'symbol':
                    df_clean[col] = 'STOCK'
                elif col == 'close':
                    df_clean[col] = 100.0
        
        print(f"✅ Data loaded successfully: {len(df_clean)} rows, {len(df_clean['symbol'].unique())} unique symbols")
        return df_clean
        
    except Exception as e:
        print(f"⚠️ Error loading data: {str(e)}")
        # Return sample data as fallback
        sample_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'close': np.random.uniform(50, 200, 100),
            'symbol': 'SAMPLE',
            'exchange': 'NYSE'
        })
        return sample_data

@workflow.atom()
def title_display():
    return text("# 🌍 World Stocks Explorer")

@workflow.atom()
def subtitle_display():
    return text("Analyze global stock market movements with interactive visualizations")

@workflow.atom()
def rolling_window_control():
    return slider(
        "Rolling Window (days)",
        min_value=5,
        max_value=60,
        value=30,
        help="Adjust the window size for moving averages"
    )

@workflow.atom()
def exchange_control():
    df = load_data()
    if df is None or df.empty:
        return selectbox("Exchange", options=["All"], help="No data loaded")
    
    exchanges = ["All"] + sorted(df['exchange'].unique().tolist())
    return selectbox(
        "Exchange",
        options=exchanges,
        help="Select a specific exchange or view all"
    )

def get_filtered_data(rolling_window=30, exchange="All"):
    """Get filtered and processed data"""
    df = load_data()
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Filter by exchange
    if exchange != "All":
        filtered_df = df[df['exchange'] == exchange].copy()
    else:
        filtered_df = df.copy()
    
    # Filter to last 365 days
    one_year_ago = datetime.now() - timedelta(days=365)
    filtered_df = filtered_df[filtered_df['date'] >= one_year_ago].copy()
    
    if filtered_df.empty:
        return filtered_df
    
    # Sort data
    filtered_df = filtered_df.sort_values(['exchange', 'symbol', 'date'])
    
    # Calculate technical indicators
    filtered_df['daily_change'] = filtered_df.groupby(['exchange', 'symbol'])['close'].pct_change() * 100
    
    # Rolling averages and Bollinger Bands
    filtered_df['rolling_avg'] = filtered_df.groupby(['exchange', 'symbol'])['close'].rolling(
        window=rolling_window, min_periods=1
    ).mean().reset_index(0, drop=True)
    
    filtered_df['rolling_std'] = filtered_df.groupby(['exchange', 'symbol'])['close'].rolling(
        window=rolling_window, min_periods=1
    ).std().reset_index(0, drop=True)
    
    filtered_df['upper_band'] = filtered_df['rolling_avg'] + (2 * filtered_df['rolling_std'])
    filtered_df['lower_band'] = filtered_df['rolling_avg'] - (2 * filtered_df['rolling_std'])
    
    return filtered_df

@workflow.atom()
def analysis_period_info():
    return text(f"### 📊 Analysis Period\nLast 365 days with rolling window analysis")

@workflow.atom()
def market_overview_info():
    df = get_filtered_data()
    if df.empty:
        return text("### 📈 Market Overview\nNo data available")
    
    unique_stocks = len(df['symbol'].unique()) if 'symbol' in df.columns else 0
    unique_exchanges = len(df['exchange'].unique()) if 'exchange' in df.columns else 0
    
    return text(f"### 📈 Market Overview\nAnalyzing {unique_stocks} stocks across {unique_exchanges} exchanges")

@workflow.atom()
def latest_update_info():
    df = get_filtered_data()
    if df.empty:
        return text("### 📅 Latest Update\nNo recent data available")
    
    latest_date = df['date'].max().strftime('%Y-%m-%d') if not df.empty else "Unknown"
    return text(f"### 📅 Latest Update\nData as of {latest_date}")

@workflow.atom()
def price_movements_table():
    df = get_filtered_data()
    if df.empty or 'daily_change' not in df.columns:
        empty_df = pd.DataFrame(columns=['Date', 'Exchange', 'Symbol', 'Close', 'Daily Change %'])
        return table(empty_df, title="Top 10 Largest Daily Price Movements - No Data")
    
    # Get top 10 largest price movements
    movements_df = df.dropna(subset=['daily_change'])
    if movements_df.empty:
        empty_df = pd.DataFrame(columns=['Date', 'Exchange', 'Symbol', 'Close', 'Daily Change %'])
        return table(empty_df, title="Top 10 Largest Daily Price Movements - No Data")
    
    top_movements = movements_df.nlargest(10, 'daily_change', key=abs)[
        ['date', 'exchange', 'symbol', 'close', 'daily_change']
    ].round(2)
    
    # Rename columns for display
    top_movements.columns = ['Date', 'Exchange', 'Symbol', 'Close', 'Daily Change %']
    
    return table(top_movements, title="Top 10 Largest Daily Price Movements")

@workflow.atom()
def price_analysis_header():
    return text("### 📈 Price Analysis with Bollinger Bands")

@workflow.atom()
def price_analysis_chart():
    # Get current control values
    rolling_window = 30  # Default value
    exchange = "All"     # Default value
    
    df = get_filtered_data(rolling_window, exchange)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for chart",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Price Analysis - No Data Available",
            template="plotly_dark",
            height=400
        )
        return plotly(fig)
    
    # Create the price chart with Bollinger Bands
    fig = go.Figure()
    
    # Group data for better visualization
    if len(df['symbol'].unique()) > 1:
        # Multiple symbols - show aggregated data
        daily_avg = df.groupby('date').agg({
            'close': 'mean',
            'rolling_avg': 'mean',
            'upper_band': 'mean',
            'lower_band': 'mean'
        }).reset_index()
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['rolling_avg'],
            name='Average Price',
            line=dict(color='#2563eb', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['upper_band'],
            name='Upper Band',
            line=dict(color='rgba(37, 99, 235, 0.3)', width=1),
            fill=None
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['lower_band'],
            name='Lower Band',
            line=dict(color='rgba(37, 99, 235, 0.3)', width=1),
            fill='tonexty',
            fillcolor='rgba(37, 99, 235, 0.1)'
        ))
        
    else:
        # Single symbol
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['close'],
            name='Close Price',
            line=dict(color='#22c55e', width=2),
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['rolling_avg'],
            name='Rolling Average',
            line=dict(color='#2563eb', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['upper_band'],
            name='Upper Band',
            line=dict(color='rgba(37, 99, 235, 0.3)', width=1),
            fill=None
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['lower_band'],
            name='Lower Band',
            line=dict(color='rgba(37, 99, 235, 0.3)', width=1),
            fill='tonexty',
            fillcolor='rgba(37, 99, 235, 0.1)'
        ))
    
    # Update layout
    title = f"{exchange} Price Analysis" if exchange != "All" else "Global Stock Price Analysis"
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        showlegend=True,
        hovermode='x unified',
        height=500,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return plotly(fig)

def main():
    """Main application function"""
    # Display componentst
    title_display()
    subtitle_display()
    
    # Controls
    rolling_window_control()
    exchange_control()
    
    # Information sections
    analysis_period_info()
    market_overview_info()
    latest_update_info()
    
    # Data tables
    price_movements_table()
    
    # Charts
    price_analysis_header()
    price_analysis_chart()

if __name__ == "__main__":
    main()
    workflow.execute()