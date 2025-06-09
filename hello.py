"""
AI Job Market Explorer 2025 - Interactive Analysis Dashboard

This Preswald application provides real-time analysis of global AI job market data,
featuring interactive visualizations and dynamic filtering capabilities.
"""

from typing import List, Optional
from datetime import datetime, timedelta

from preswald import connect, get_df, query, table, text, plotly, slider, selectbox
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Initialize connection and load data
connect()  # Initialize connection to preswald.toml data sources
df = get_df("ai_job_dataset_csv")  # Load data from configured source

# 2. Basic data processing
text("# AI Job Market Analytics")
text("Interactive analysis of global AI job market data")

# Show basic info
text(f"📊 **Dataset**: {len(df):,} job records loaded")

# Clean salary data
df["salary_usd"] = pd.to_numeric(df["salary_usd"], errors='coerce')
df = df.dropna(subset=['salary_usd'])

# 3. Interactive controls
text("## Filters")
experience_filter = selectbox("Experience Level", options=["All", "EN", "MI", "SE", "EX"])
salary_min = slider("Minimum Salary (USD)", min_val=0, max_val=200000, default=50000, step=10000)
salary_max = slider("Maximum Salary (USD)", min_val=50000, max_val=300000, default=200000, step=10000)

# 4. Query and filter data
if experience_filter != "All":
    filtered_df = df[(df["experience_level"] == experience_filter) & 
                     (df["salary_usd"] >= salary_min) & 
                     (df["salary_usd"] <= salary_max)]
else:
    filtered_df = df[(df["salary_usd"] >= salary_min) & (df["salary_usd"] <= salary_max)]

# 5. Display results
text(f"## Results ({len(filtered_df)} jobs found)")

if not filtered_df.empty:
    # Summary statistics
    avg_salary = int(filtered_df["salary_usd"].mean())
    text(f"**Average Salary**: ${avg_salary:,}")
    
    # Sample data table
    text("### Sample Job Records")
    sample_data = filtered_df[["job_title", "salary_usd", "experience_level", "company_location"]].head(10)
    table(sample_data, title="Job Records")
    
    # 6. Visualizations
    text("### Salary Distribution")
    fig_hist = px.histogram(
        filtered_df, 
        x="salary_usd", 
        nbins=20,
        title="Salary Distribution",
        labels={"salary_usd": "Salary (USD)", "count": "Number of Jobs"}
    )
    plotly(fig_hist)
    
    # Top locations
    text("### Top Locations")
    location_counts = filtered_df["company_location"].value_counts().head(10)
    fig_bar = px.bar(
        x=location_counts.index,
        y=location_counts.values,
        title="Jobs by Location",
        labels={"x": "Location", "y": "Number of Jobs"}
    )
    plotly(fig_bar)
    
else:
    text("No jobs found with the selected filters.") 