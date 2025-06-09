# 🌍 World Stocks Explorer

An elegant, real-time analysis dashboard for global stock market data, built with Preswald.

![Dashboard Preview](images/dashboard-preview.png)

## 📊 Features

- **Interactive Analysis**
  - Dynamic rolling window (5-60 days) for trend analysis
  - Exchange-specific or global market view
  - Real-time data filtering and visualization

- **Advanced Analytics**
  - Bollinger Bands for volatility analysis
  - Top 10 largest daily price movements
  - 365-day historical data view
  - Rolling averages with standard deviation bands

- **Modern UI/UX**
  - Dark mode interface
  - Responsive layout
  - Interactive charts with hover details
  - Clean, intuitive controls

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip3 install -r requirements.txt
   ```

2. **Run the App**
   ```bash
   preswald run
   ```
   Or use your IDE's Preview functionality.

## 📁 Project Structure

```
World-Stocks-Explorer/
├── data/                    # Data directory
│   └── World-Stock-Prices-Dataset.csv
├── static/                  # Static assets
│   └── stocks.ico
├── images/                  # Documentation images
├── script.py               # Main application code
├── preswald.toml          # Preswald configuration
├── pyproject.toml         # Python package configuration
└── README.md              # This file
```

## 📈 Dataset

Source: [World Stock Prices Dataset](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs) (placeholder URL)

The dataset includes:
- Daily closing prices
- Multiple global exchanges
- Historical data spanning multiple years
- Volume and price information

## 🔮 Future Enhancements

1. **Technical Analysis**
   - Add RSI, MACD, and other technical indicators
   - Implement custom indicator builder

2. **Market Insights**
   - Sector correlation analysis
   - Market sentiment integration
   - News impact analysis

3. **Performance**
   - Implement data caching
   - Add real-time data streaming
   - Optimize query performance

## 🤝 Contributing

This is an assessment project for Structured Labs. For questions or feedback, please contact the candidate.

---

Git commit: "initial world-stocks demo" 