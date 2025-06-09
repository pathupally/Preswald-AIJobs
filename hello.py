"""
AI Job Market Explorer - Interactive Analysis Dashboard

This Preswald application provides real-time analysis of global AI job market data,
featuring salary trends, skill demands, and geographic distribution insights.
"""

from typing import List, Optional
from datetime import datetime, timedelta
import os

from preswald import connect, get_df, query, table, text, plotly, slider, selectbox, multiselect, get_workflow
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
    """Load and preprocess AI job market data"""
    try:
        # Try different possible file paths
        possible_paths = [
            "AI-Job-Market-Dataset.csv",
            "data/AI-Job-Market-Dataset.csv",
            "./data/AI-Job-Market-Dataset.csv",
            "main_dataset.csv",
            "data/main_dataset.csv"
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
                df_raw = get_df("main_dataset.csv")
            except:
                print("⚠️ Could not find data file. Creating sample data...")
                # Create comprehensive sample data based on dataset description
                np.random.seed(42)
                
                job_titles = [
                    'ML Engineer', 'Data Scientist', 'AI Research Scientist', 'AI Engineer',
                    'Deep Learning Engineer', 'Computer Vision Engineer', 'NLP Engineer',
                    'Data Engineer', 'AI Product Manager', 'Machine Learning Researcher',
                    'AI Consultant', 'Data Analyst', 'AI Architect', 'MLOps Engineer'
                ]
                
                countries = [
                    'United States', 'Germany', 'United Kingdom', 'Canada', 'France',
                    'Netherlands', 'Switzerland', 'Australia', 'India', 'Singapore',
                    'Sweden', 'Israel', 'Japan', 'South Korea', 'China'
                ]
                
                experience_levels = ['EN', 'MI', 'SE', 'EX']
                employment_types = ['FT', 'PT', 'CT', 'FL']
                company_sizes = ['S', 'M', 'L']
                
                data = []
                for i in range(1000):  # Generate 1000 sample jobs
                    exp_level = np.random.choice(experience_levels, p=[0.2, 0.4, 0.3, 0.1])
                    
                    # Salary based on experience level and location
                    base_salaries = {'EN': 75000, 'MI': 105000, 'SE': 140000, 'EX': 180000}
                    country = np.random.choice(countries)
                    
                    # Country salary multipliers
                    country_multipliers = {
                        'United States': 1.0, 'Switzerland': 1.2, 'Germany': 0.85,
                        'United Kingdom': 0.9, 'Canada': 0.88, 'Australia': 0.92,
                        'Netherlands': 0.87, 'France': 0.82, 'Singapore': 0.95,
                        'Sweden': 0.85, 'India': 0.3, 'China': 0.4, 'Japan': 0.75,
                        'South Korea': 0.6, 'Israel': 0.85
                    }
                    
                    base_salary = base_salaries[exp_level]
                    multiplier = country_multipliers.get(country, 0.8)
                    salary = int(base_salary * multiplier * np.random.uniform(0.8, 1.4))
                    
                    data.append({
                        'job_id': f'AI{i+1:04d}',
                        'job_title': np.random.choice(job_titles),
                        'salary_usd': salary,
                        'salary_currency': 'USD',
                        'experience_level': exp_level,
                        'employment_type': np.random.choice(employment_types, p=[0.8, 0.05, 0.1, 0.05]),
                        'company_location': country,
                        'company_size': np.random.choice(company_sizes, p=[0.3, 0.4, 0.3]),
                        'remote_ratio': np.random.choice([0, 50, 100], p=[0.3, 0.4, 0.3]),
                        'years_experience': np.random.randint(0, 15),
                        'industry': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Retail', 'Automotive', 'Research'])
                    })
                
                df_raw = pd.DataFrame(data)
        
        # Ensure we have required columns
        required_columns = ['job_id', 'job_title', 'salary_usd', 'experience_level', 
                          'employment_type', 'company_location', 'company_size']
        
        for col in required_columns:
            if col not in df_raw.columns:
                print(f"⚠️ Warning: Missing column {col}")
                if col == 'salary_usd':
                    df_raw[col] = 100000
                elif col == 'experience_level':
                    df_raw[col] = 'MI'
                else:
                    df_raw[col] = 'Unknown'
        
        # Clean the data
        df_clean = df_raw.dropna(subset=['salary_usd'])
        df_clean = df_clean[df_clean['salary_usd'] > 0]  # Remove invalid salaries
        
        print(f"✅ Data loaded successfully: {len(df_clean)} jobs, {len(df_clean['job_title'].unique())} unique roles")
        return df_clean
        
    except Exception as e:
        print(f"⚠️ Error loading data: {str(e)}")
        # Return minimal sample data as fallback
        return pd.DataFrame({
            'job_id': ['AI001'],
            'job_title': ['Data Scientist'],
            'salary_usd': [100000],
            'experience_level': ['MI'],
            'employment_type': ['FT'],
            'company_location': ['United States'],
            'company_size': ['M']
        })

@workflow.atom()
def title_display():
    return text("# 🤖 AI Job Market Explorer 2025")

@workflow.atom()
def subtitle_display():
    return text("Comprehensive analysis of global AI job opportunities, salaries, and market trends")

@workflow.atom()
def experience_filter():
    df = load_data()
    if df is None or df.empty:
        return selectbox("Experience Level", options=["All"], help="No data loaded")
    
    exp_mapping = {
        'EN': 'Entry Level',
        'MI': 'Mid Level', 
        'SE': 'Senior Level',
        'EX': 'Executive Level'
    }
    
    levels = ["All"] + [f"{code} - {exp_mapping.get(code, code)}" 
                       for code in sorted(df['experience_level'].unique())]
    
    return selectbox(
        "Experience Level",
        options=levels,
        help="Filter by experience level"
    )

@workflow.atom()
def location_filter():
    df = load_data()
    if df is None or df.empty:
        return selectbox("Location", options=["All"], help="No data loaded")
    
    locations = ["All"] + sorted(df['company_location'].unique().tolist())
    return selectbox(
        "Location",
        options=locations,
        help="Filter by company location"
    )

@workflow.atom()
def salary_range_filter():
    df = load_data()
    if df is None or df.empty:
        return text("### 💰 Salary Range: No data available")
    
    min_salary = int(df['salary_usd'].min())
    max_salary = int(df['salary_usd'].max())
    
    return slider(
        "Minimum Salary (USD)",
        min_value=min_salary,
        max_value=max_salary,
        value=min_salary,
        help="Filter jobs by minimum salary"
    )

def get_filtered_data(experience="All", location="All", min_salary=0):
    """Get filtered data based on current selections"""
    df = load_data()
    if df is None or df.empty:
        return pd.DataFrame()
    
    filtered_df = df.copy()
    
    # Filter by experience level
    if experience != "All" and " - " in experience:
        exp_code = experience.split(" - ")[0]
        filtered_df = filtered_df[filtered_df['experience_level'] == exp_code]
    
    # Filter by location
    if location != "All":
        filtered_df = filtered_df[filtered_df['company_location'] == location]
    
    # Filter by salary
    filtered_df = filtered_df[filtered_df['salary_usd'] >= min_salary]
    
    return filtered_df

@workflow.atom()
def market_overview():
    df = get_filtered_data()
    if df.empty:
        return text("### 📊 Market Overview\nNo data matches current filters")
    
    total_jobs = len(df)
    avg_salary = df['salary_usd'].mean()
    unique_companies = len(df['company_location'].unique())
    
    return text(f"""### 📊 Market Overview
**{total_jobs:,}** job postings analyzed  
**${avg_salary:,.0f}** average salary  
**{unique_companies}** countries represented  
""")

@workflow.atom()
def salary_by_experience_chart():
    df = get_filtered_data()
    if df.empty:
        return text("No data available for salary analysis")
    
    # Calculate average salary by experience level
    exp_mapping = {
        'EN': 'Entry Level',
        'MI': 'Mid Level', 
        'SE': 'Senior Level',
        'EX': 'Executive Level'
    }
    
    salary_by_exp = df.groupby('experience_level')['salary_usd'].agg(['mean', 'count']).reset_index()
    salary_by_exp['experience_label'] = salary_by_exp['experience_level'].map(exp_mapping)
    salary_by_exp = salary_by_exp.sort_values('mean')
    
    fig = px.bar(
        salary_by_exp,
        x='experience_label',
        y='mean',
        title='Average Salary by Experience Level',
        labels={'mean': 'Average Salary (USD)', 'experience_label': 'Experience Level'},
        color='mean',
        color_continuous_scale='viridis',
        text='mean'
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        height=400,
        yaxis_tickformat='$,.0f'
    )
    
    return plotly(fig)

@workflow.atom()
def top_locations_chart():
    df = get_filtered_data()
    if df.empty:
        return text("No data available for location analysis")
    
    # Top 10 locations by job count
    top_locations = df['company_location'].value_counts().head(10).reset_index()
    top_locations.columns = ['location', 'job_count']
    
    fig = px.bar(
        top_locations,
        x='job_count',
        y='location',
        orientation='h',
        title='Top 10 Countries by Job Postings',
        labels={'job_count': 'Number of Jobs', 'location': 'Country'},
        color='job_count',
        color_continuous_scale='plasma'
    )
    
    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return plotly(fig)

@workflow.atom()
def salary_distribution_chart():
    df = get_filtered_data()
    if df.empty:
        return text("No data available for salary distribution")
    
    fig = px.histogram(
        df,
        x='salary_usd',
        nbins=30,
        title='Salary Distribution',
        labels={'salary_usd': 'Salary (USD)', 'count': 'Number of Jobs'},
        color_discrete_sequence=['#00d4aa']
    )
    
    fig.update_layout(
        template='plotly_dark',
        height=400,
        xaxis_tickformat='$,.0f'
    )
    
    return plotly(fig)

@workflow.atom()
def remote_work_analysis():
    df = get_filtered_data()
    if df.empty or 'remote_ratio' not in df.columns:
        return text("No remote work data available")
    
    remote_mapping = {
        0: 'On-site',
        50: 'Hybrid',
        100: 'Fully Remote'
    }
    
    df['remote_label'] = df['remote_ratio'].map(remote_mapping)
    remote_dist = df['remote_label'].value_counts().reset_index()
    remote_dist.columns = ['work_type', 'count']
    
    fig = px.pie(
        remote_dist,
        values='count',
        names='work_type',
        title='Remote Work Distribution',
        color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1']
    )
    
    fig.update_layout(
        template='plotly_dark',
        height=400
    )
    
    return plotly(fig)

@workflow.atom()
def top_job_titles_table():
    df = get_filtered_data()
    if df.empty:
        return table(pd.DataFrame(), title="Top Job Titles - No Data")
    
    # Top job titles with average salary
    job_stats = df.groupby('job_title').agg({
        'salary_usd': ['mean', 'count'],
        'job_id': 'count'
    }).reset_index()
    
    job_stats.columns = ['Job Title', 'Avg Salary', 'Salary Count', 'Total Postings']
    job_stats = job_stats.sort_values('Total Postings', ascending=False).head(10)
    job_stats['Avg Salary'] = job_stats['Avg Salary'].round(0).astype(int)
    job_stats = job_stats[['Job Title', 'Total Postings', 'Avg Salary']]
    
    return table(job_stats, title="Top 10 Most In-Demand AI Job Titles")

@workflow.atom()
def company_size_analysis():
    df = get_filtered_data()
    if df.empty or 'company_size' not in df.columns:
        return text("No company size data available")
    
    size_mapping = {
        'S': 'Small (<50)',
        'M': 'Medium (50-250)',
        'L': 'Large (>250)'
    }
    
    df['size_label'] = df['company_size'].map(size_mapping)
    size_salary = df.groupby('size_label')['salary_usd'].mean().reset_index()
    
    fig = px.bar(
        size_salary,
        x='size_label',
        y='salary_usd',
        title='Average Salary by Company Size',
        labels={'salary_usd': 'Average Salary (USD)', 'size_label': 'Company Size'},
        color='salary_usd',
        color_continuous_scale='blues'
    )
    
    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        height=400,
        yaxis_tickformat='$,.0f'
    )
    
    return plotly(fig)

def main():
    """Main application function"""
    # Header
    title_display()
    subtitle_display()
    
    # Filters
    experience_filter()
    location_filter()
    salary_range_filter()
    
    # Overview
    market_overview()
    
    # Charts and analysis
    salary_by_experience_chart()
    top_locations_chart()
    salary_distribution_chart()
    remote_work_analysis()
    company_size_analysis()
    
    # Data table
    top_job_titles_table()

if __name__ == "__main__":
    main()
    workflow.execute()