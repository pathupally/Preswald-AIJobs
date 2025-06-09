"""
AI Job Market Explorer - Interactive Analysis Dashboard
Built with Preswald following best practices
"""

from preswald import connect, get_df, query, table, text, plotly, slider, selectbox
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Initialize Preswald connection
connect()

# Load and sample the dataset for better performance
def load_sample_data():
    """Load a sample of the dataset for faster performance"""
    try:
        # Try to load the full dataset
        df = get_df("AI-Job-Market-Dataset")
        
        # Sample 2000 rows for better performance
        if len(df) > 2000:
            df = df.sample(n=2000, random_state=42)
            
        print(f"✅ Loaded {len(df)} job records")
        return df
    except:
        try:
            # Try alternative names
            df = get_df("main_dataset")
            if len(df) > 2000:
                df = df.sample(n=2000, random_state=42)
            return df
        except:
            # Create minimal sample data as fallback
            return pd.DataFrame({
                'job_title': ['Data Scientist', 'ML Engineer', 'AI Researcher'] * 100,
                'salary_usd': [120000, 140000, 160000] * 100,
                'experience_level': ['MI', 'SE', 'EX'] * 100,
                'company_location': ['United States', 'Germany', 'Canada'] * 100,
                'company_size': ['M', 'L', 'S'] * 100,
                'remote_ratio': [0, 50, 100] * 100,
                'employment_type': ['FT'] * 300
            })

# Load data once
df = load_sample_data()

# Title and description
text("# 🤖 AI Job Market Explorer 2025")
text("**Interactive analysis of global AI job opportunities and salary trends**")

# Interactive controls
text("## 🎛️ Filters")

# Experience level filter
exp_options = ["All"] + sorted(df['experience_level'].unique().tolist())
selected_experience = selectbox("Experience Level", options=exp_options)

# Location filter  
location_options = ["All"] + sorted(df['company_location'].unique().tolist())
selected_location = selectbox("Company Location", options=location_options)

# Salary range filter
min_salary = int(df['salary_usd'].min())
max_salary = int(df['salary_usd'].max())
salary_threshold = slider("Minimum Salary (USD)", 
                         min_value=min_salary, 
                         max_value=max_salary, 
                         value=min_salary)

# Apply filters using query
def get_filtered_data():
    conditions = []
    
    if selected_experience != "All":
        conditions.append(f"experience_level = '{selected_experience}'")
    
    if selected_location != "All":
        conditions.append(f"company_location = '{selected_location}'")
    
    conditions.append(f"salary_usd >= {salary_threshold}")
    
    if conditions:
        where_clause = " AND ".join(conditions)
        sql = f"SELECT * FROM df WHERE {where_clause}"
        return query(sql, "df")
    else:
        return df

filtered_df = get_filtered_data()

# Market overview
text("## 📊 Market Overview")
text(f"""
- **{len(filtered_df):,}** job postings match your filters
- **${filtered_df['salary_usd'].mean():,.0f}** average salary
- **{len(filtered_df['company_location'].unique())}** countries represented
- **{len(filtered_df['job_title'].unique())}** unique job titles
""")

# Chart 1: Salary by Experience Level
text("## 💰 Salary Analysis")
salary_by_exp = filtered_df.groupby('experience_level')['salary_usd'].mean().reset_index()
exp_mapping = {'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'}
salary_by_exp['level'] = salary_by_exp['experience_level'].map(exp_mapping)

fig1 = px.bar(salary_by_exp, x='level', y='salary_usd',
              title='Average Salary by Experience Level',
              labels={'salary_usd': 'Average Salary (USD)', 'level': 'Experience Level'},
              color='salary_usd', color_continuous_scale='viridis')
fig1.update_layout(template='plotly_dark', height=400)
plotly(fig1)

# Chart 2: Geographic Distribution
text("## 🌍 Geographic Distribution")
location_counts = filtered_df['company_location'].value_counts().head(10).reset_index()
location_counts.columns = ['Country', 'Job Count']

fig2 = px.bar(location_counts, x='Job Count', y='Country', orientation='h',
              title='Top 10 Countries by Job Postings',
              color='Job Count', color_continuous_scale='plasma')
fig2.update_layout(template='plotly_dark', height=500, yaxis={'categoryorder': 'total ascending'})
plotly(fig2)

# Chart 3: Salary Distribution
text("## 📈 Salary Distribution")
fig3 = px.histogram(filtered_df, x='salary_usd', nbins=25,
                    title='Distribution of AI Job Salaries',
                    labels={'salary_usd': 'Salary (USD)', 'count': 'Number of Jobs'},
                    color_discrete_sequence=['#00d4aa'])
fig3.update_layout(template='plotly_dark', height=400)
plotly(fig3)

# Chart 4: Remote Work Analysis
if 'remote_ratio' in filtered_df.columns:
    text("## 🏠 Remote Work Trends")
    remote_mapping = {0: 'On-site', 50: 'Hybrid', 100: 'Fully Remote'}
    filtered_df['work_type'] = filtered_df['remote_ratio'].map(remote_mapping)
    remote_counts = filtered_df['work_type'].value_counts().reset_index()
    remote_counts.columns = ['Work Type', 'Count']
    
    fig4 = px.pie(remote_counts, values='Count', names='Work Type',
                  title='Remote Work Distribution',
                  color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    fig4.update_layout(template='plotly_dark', height=400)
    plotly(fig4)

# Chart 5: Company Size vs Salary
if 'company_size' in filtered_df.columns:
    text("## 🏢 Company Size Analysis")
    size_mapping = {'S': 'Small (<50)', 'M': 'Medium (50-250)', 'L': 'Large (>250)'}
    filtered_df['size_label'] = filtered_df['company_size'].map(size_mapping)
    size_salary = filtered_df.groupby('size_label')['salary_usd'].mean().reset_index()
    
    fig5 = px.bar(size_salary, x='size_label', y='salary_usd',
                  title='Average Salary by Company Size',
                  labels={'salary_usd': 'Average Salary (USD)', 'size_label': 'Company Size'},
                  color='salary_usd', color_continuous_scale='blues')
    fig5.update_layout(template='plotly_dark', height=400)
    plotly(fig5)

# Chart 6: Job Title Frequency
text("## 🎯 Most In-Demand Roles")
job_counts = filtered_df['job_title'].value_counts().head(15).reset_index()
job_counts.columns = ['Job Title', 'Frequency']

fig6 = px.bar(job_counts, x='Frequency', y='Job Title', orientation='h',
              title='Top 15 Most Posted AI Job Titles',
              color='Frequency', color_continuous_scale='viridis')
fig6.update_layout(template='plotly_dark', height=600, yaxis={'categoryorder': 'total ascending'})
plotly(fig6)

# Chart 7: Salary vs Experience Scatter
text("## 🎯 Salary vs Experience Correlation")
if 'years_experience' in filtered_df.columns:
    fig7 = px.scatter(filtered_df, x='years_experience', y='salary_usd', 
                      color='experience_level',
                      title='Salary vs Years of Experience',
                      labels={'years_experience': 'Years of Experience', 'salary_usd': 'Salary (USD)'},
                      hover_data=['job_title', 'company_location'])
    fig7.update_layout(template='plotly_dark', height=500)
    plotly(fig7)

# Chart 8: Employment Type Distribution
text("## 💼 Employment Types")
emp_counts = filtered_df['employment_type'].value_counts().reset_index()
emp_counts.columns = ['Employment Type', 'Count']
emp_mapping = {'FT': 'Full-time', 'PT': 'Part-time', 'CT': 'Contract', 'FL': 'Freelance'}
emp_counts['Type Label'] = emp_counts['Employment Type'].map(emp_mapping)

fig8 = px.pie(emp_counts, values='Count', names='Type Label',
              title='Employment Type Distribution',
              color_discrete_sequence=['#2563eb', '#7c3aed', '#dc2626', '#059669'])
fig8.update_layout(template='plotly_dark', height=400)
plotly(fig8)

# Chart 9: Salary Boxplot by Location (Top 5)
text("## 🌐 Salary Range by Top Locations")
top_locations = filtered_df['company_location'].value_counts().head(5).index.tolist()
top_location_data = filtered_df[filtered_df['company_location'].isin(top_locations)]

fig9 = px.box(top_location_data, x='company_location', y='salary_usd',
              title='Salary Distribution in Top 5 Markets',
              labels={'company_location': 'Country', 'salary_usd': 'Salary (USD)'})
fig9.update_layout(template='plotly_dark', height=500)
plotly(fig9)

# Chart 10: Heatmap of Experience vs Company Size
text("## 🔥 Experience Level vs Company Size Heatmap")
if 'company_size' in filtered_df.columns:
    heatmap_data = filtered_df.groupby(['experience_level', 'company_size']).size().reset_index(name='count')
    heatmap_pivot = heatmap_data.pivot(index='experience_level', columns='company_size', values='count').fillna(0)
    
    fig10 = px.imshow(heatmap_pivot, 
                      title='Job Distribution: Experience Level vs Company Size',
                      color_continuous_scale='viridis',
                      aspect='auto')
    fig10.update_layout(template='plotly_dark', height=400)
    plotly(fig10)

# Data table
text("## 📋 Job Listings Sample")
display_columns = ['job_title', 'salary_usd', 'experience_level', 'company_location', 'company_size']
sample_data = filtered_df[display_columns].head(20)
table(sample_data, title=f"Sample of {len(filtered_df)} Matching Jobs")

# Summary statistics table
text("## 📊 Summary Statistics")
stats_df = filtered_df.groupby('experience_level').agg({
    'salary_usd': ['count', 'mean', 'median', 'min', 'max']
}).round(0)
stats_df.columns = ['Count', 'Avg Salary', 'Median Salary', 'Min Salary', 'Max Salary']
table(stats_df.reset_index(), title="Salary Statistics by Experience Level")