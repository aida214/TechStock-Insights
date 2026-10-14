# 📈 TechStock Insights
### Interactive Stock Market Analysis & Portfolio Risk Dashboard

TechStock Insights is an interactive data analytics project designed to explore historical stock market performance, compare technology stocks, analyze investment risk, and simulate potential portfolio outcomes. Built with Python and Streamlit, it transforms financial data into meaningful visual insights through an easy-to-use dashboard.

The project focuses on making stock market data easier to understand through interactive charts, financial performance metrics, risk analysis, and downloadable reports.

## 🎯 Project Objectives

- Analyze historical stock price movements and returns.
- Compare the performance of major technology companies.
- Evaluate investment risk using statistical measures.
- Explore portfolio allocation and diversification.
- Simulate potential future portfolio outcomes using Monte Carlo simulation.
- Generate downloadable reports for further analysis.

## ✨ Key Features

### 📊 Interactive Stock Analysis
- Retrieve historical stock market data using Yahoo Finance.
- Analyze multiple technology stocks, including Apple (AAPL), Microsoft (MSFT), Alphabet (GOOGL), and Amazon (AMZN).
- Visualize stock prices, returns, and historical trends.
- Compare the performance of selected stocks over a chosen time period.

### 📈 Performance Metrics
- Calculate cumulative returns and daily returns.
- Compare overall stock performance.
- Visualize historical price movements and performance trends.

### ⚠️ Risk Analysis
- Evaluate historical volatility.
- Analyze maximum drawdown.
- Compare risk and return across different stocks.
- Understand how historical market fluctuations affect investment performance.

### 💼 Portfolio Analysis
- Experiment with different portfolio allocations.
- Explore the relationship between portfolio risk and return.
- Compare potential portfolio outcomes using historical data.

### 🎲 Monte Carlo Simulation
- Simulate possible portfolio value trajectories.
- Explore a range of hypothetical investment outcomes.
- Visualize uncertainty in potential future portfolio performance.

### 📥 Downloadable Reports
- Export analysis results to CSV and Excel.
- Generate an HTML report containing key findings and visualizations.
- Save results for presentations, documentation, and further analysis.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations and simulations |
| yfinance | Retrieving historical stock market data |
| Plotly | Interactive data visualizations |
| Streamlit | Interactive web dashboard |
| OpenPyXL | Excel file export |

## 📂 Project Structure

```text
TechStock-Insights/
│
├── TechStock_Insights.ipynb   # Jupyter Notebook analysis
├── app.py                     # Streamlit dashboard
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```


## 🚀 Getting Started

Follow these steps to run TechStock Insights on your computer.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/TechStock-Insights.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Navigate to the Project Folder

```bash
cd TechStock-Insights
```

### 3. Install Dependencies

Make sure Python is installed, then run:

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the Dashboard

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL that you can open in your web browser.

## 📦 Requirements

The `requirements.txt` file should contain:

```text
streamlit
yfinance
pandas
numpy
plotly
openpyxl
```

## 📓 Jupyter Notebook

The included Jupyter Notebook provides a space to explore the data analysis process, experiment with calculations, and understand the methods used in the dashboard.

You can open it using Jupyter Notebook, JupyterLab, or Google Colab.

## 📊 Data Source

Historical stock market data is retrieved through the `yfinance` Python library, which provides access to Yahoo Finance data.

Data availability, historical coverage, and retrieval may vary. The project depends on an internet connection when downloading fresh market data.

## 🔮 Future Improvements

Potential enhancements include:

- Adding more stocks, sectors, and market indices.
- Incorporating additional financial indicators.
- Improving portfolio optimization techniques.
- Adding customizable benchmark comparisons.
- Introducing more advanced forecasting models.
- Enhancing automated report generation.
- Deploying the dashboard online for public access.

## ⚠️ Disclaimer

TechStock Insights is an educational data analytics project. Its visualizations, historical metrics, and simulations are intended for learning and exploration, not as financial advice or investment recommendations.

Historical performance and simulated outcomes do not guarantee future results.

## 👩‍💻 Author

**Aiyda Syed**  
BS Data Science Student | Data Analytics | Machine Learning

GitHub: [@aida214](https://github.com/aida214)

---


