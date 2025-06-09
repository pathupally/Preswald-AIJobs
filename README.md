# 🤖 AI Job Market Analytics Dashboard

> **Interactive insights into the global AI employment landscape**

[![Preswald](https://img.shields.io/badge/Built%20with-Preswald-00d4aa?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh2dG1sIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDkuNzRMMTIgMTZMMTAuOTEgOS43NEw0IDlMMTAuOTEgOC4yNkwxMiAyWiIgZmlsbD0iIzAwZDRhYSIvPgo8L3N2Zz4K)](https://github.com/StructuredLabs/preswald)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📊 Overview

A sophisticated analytics dashboard that provides real-time insights into the global AI job market. Built with **Preswald** for seamless interactivity and **Plotly** for stunning visualizations.

### ✨ Key Features

- 🎯 **Interactive Filtering** - Filter by experience level, salary range, and location
- 📈 **Dynamic Visualizations** - Real-time charts and graphs powered by Plotly
- 🌍 **Global Coverage** - Data from 15,000+ job postings across multiple countries
- 💰 **Salary Analytics** - Comprehensive salary analysis by experience and location
- 📱 **Responsive Design** - Works seamlessly across all devices

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd World-Stocks-Explorer

# Install dependencies
pip install preswald plotly pandas

# Run the application
preswald run
```

The dashboard will be available at `http://localhost:8501`

---

## 📈 Dashboard Features

### Interactive Controls
- **Experience Level Filter**: EN (Entry), MI (Mid), SE (Senior), EX (Executive)
- **Salary Range Sliders**: Dynamic filtering from $0 to $300,000
- **Real-time Updates**: Instant visualization updates based on selections

### Analytics Components
- **Salary Distribution Histogram**: Visualize salary patterns across the market
- **Geographic Job Distribution**: Top locations by job count
- **Sample Job Records Table**: Detailed view of filtered results
- **Summary Statistics**: Average salaries and job counts

---

## 📊 Dataset Information

| Metric | Value |
|--------|-------|
| **Total Records** | 15,000+ job postings |
| **Data Source** | Global AI job market analysis |
| **Time Period** | 2024-2025 |
| **Coverage** | Multiple countries and industries |
| **Fields** | 19 comprehensive data columns |

### Data Fields
- `job_title` - Position title and role
- `salary_usd` - Annual salary in USD
- `experience_level` - EN/MI/SE/EX classification
- `company_location` - Geographic location
- `remote_ratio` - Remote work percentage
- `required_skills` - Technical skill requirements
- `company_size` - Organization scale
- `industry` - Business sector

---

## 🛠️ Technical Architecture

### Built With
- **[Preswald](https://github.com/StructuredLabs/preswald)** - Reactive data app framework
- **[Plotly](https://plotly.com/python/)** - Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[Python](https://python.org)** - Core programming language

### Architecture Highlights
- **Reactive Workflow**: Automatic updates based on user interactions
- **Component-Based UI**: Modular design for easy maintenance
- **Data-Driven**: Real-time filtering and analysis
- **Performance Optimized**: Efficient data processing and rendering

---

## 📱 Screenshots

<details>
<summary>🎯 Interactive Dashboard</summary>

![Dashboard Overview](images/dashboard.png)

</details>

<details>
<summary>📊 Salary Analytics</summary>

![Salary Analysis](images/salary-analysis.png)

</details>

---

## 🔧 Configuration

The application is configured via `preswald.toml`:

```toml
[project]
title = "AI Job Market Analytics App"
version = "0.1.0"
port = 8501
entrypoint = "hello.py"

[data.ai_job_dataset_csv]
type = "csv"
path = "data/ai_job_dataset.csv"
```

---

## 🎯 Use Cases

### For Job Seekers
- **Salary Research**: Understand market rates for your experience level
- **Location Analysis**: Compare opportunities across different countries
- **Skill Mapping**: Identify in-demand technical skills

### For Employers
- **Market Intelligence**: Benchmark compensation against industry standards
- **Talent Acquisition**: Understand geographic talent distribution
- **Competitive Analysis**: Analyze competitor hiring patterns

### For Analysts
- **Market Trends**: Track salary evolution over time
- **Geographic Insights**: Understand regional market dynamics
- **Skill Demand**: Identify emerging technical requirements

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/World-Stocks-Explorer.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run the development server
preswald run
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Preswald Team** - For building an incredible reactive data app framework
  - [@amrutha97](https://github.com/amrutha97) - Co-founder
  - [@shivam-singhal](https://github.com/shivam-singhal) - Co-founder
- **Open Source Community** - For the amazing tools that make this possible
- **Data Contributors** - For providing comprehensive AI job market insights

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/World-Stocks-Explorer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/World-Stocks-Explorer/discussions)
- **Email**: your-email@example.com

---

<div align="center">

**Made with ❤️ by the AI Job Market Analytics Team**

[![GitHub stars](https://img.shields.io/github/stars/your-username/World-Stocks-Explorer?style=social)](https://github.com/your-username/World-Stocks-Explorer)
[![GitHub forks](https://img.shields.io/github/forks/your-username/World-Stocks-Explorer?style=social)](https://github.com/your-username/World-Stocks-Explorer)

</div>