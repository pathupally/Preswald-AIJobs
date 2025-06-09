🌍 World Stocks Explorer
An elegant, real-time analysis dashboard for global stock market data, built with Preswald.



🚀 Quick Start
Automated Setup (Recommended)
bash
# Clone or download the project
# Navigate to project directory
cd World-Stocks-Explorer

# Run the setup script
python3 setup.py

# Activate virtual environment
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Run the application
preswald run
Manual Setup
bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data (if you don't have the dataset)
python generate_sample_data.py

# 4. Run the application
preswald run
📊 Features
Interactive Analysis
Dynamic Rolling Window: Adjustable 5-60 day analysis periods
Exchange Filtering: View specific exchanges or global markets
Real-time Controls: Interactive sliders and filters
Responsive Design: Works on desktop and mobile
Advanced Analytics
Bollinger Bands: Volatility analysis with upper/lower bands
Price Movements: Top 10 largest daily price changes
Technical Indicators: Rolling averages and standard deviations
Historical Data: 365-day historical analysis
Modern UI/UX
Dark Theme: Professional dark mode interface
Interactive Charts: Hover details and zoom capabilities
Clean Layout: Intuitive navigation and controls
Real-time Updates: Dynamic data visualization
📁 Project Structure
World-Stocks-Explorer/
├── data/                           # Data directory
│   └── World-Stock-Prices-Dataset.csv
├── static/                         # Static assets
│   ├── stocks.ico
│   └── stocks.svg
├── images/                         # Documentation images
├── hello.py                        # Main application (FIXED)
├── setup.py                        # Automated setup script
├── generate_sample_data.py         # Sample data generator
├── preswald.toml                   # Preswald configuration
├── pyproject.toml                  # Python package configuration
├── requirements.txt                # Python dependencies (UPDATED)
└── README.md                       # This file
🔧 Technical Details
Key Fixes Applied
Workflow Decorators: Fixed @workflow.atom() syntax
Data Loading: Robust CSV loading with fallback options
Error Handling:
