import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io

st.set_page_config(
    page_title="TechStock Insights",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #f1f5f9;
}
[data-testid="stMetric"] {
    background: #162235;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #26364c;
}
h1, h2, h3 {
    color: #65d6c4;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 TechStock Insights")
st.write("Interactive stock market analytics and portfolio dashboard.")
st.caption("Historical market data provided by Yahoo Finance. Educational use only.")

# SIDEBAR
st.sidebar.header("Dashboard Settings")

available_stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN",
    "NVDA", "META", "TSLA", "NFLX",
    "AMD", "INTC"
]

tickers = st.sidebar.multiselect(
    "Select stocks",
    available_stocks,
    default=["AAPL", "MSFT", "GOOGL", "AMZN"]
)

start_date = st.sidebar.date_input(
    "Start date",
    value=pd.Timestamp("2020-01-01").date()
)

end_date = st.sidebar.date_input(
    "End date",
    value=pd.Timestamp.today().date()
)

investment = st.sidebar.number_input(
    "Starting portfolio ($)",
    min_value=100,
    max_value=10000000,
    value=10000,
    step=500
)

if not tickers:
    st.warning("Select at least one stock from the sidebar.")
    st.stop()

if start_date >= end_date:
    st.error("End date must be later than start date.")
    st.stop()

# DOWNLOAD STOCK DATA
@st.cache_data(ttl=3600)
def download_data(tickers, start, end):
    raw = yf.download(
        tickers,
        start=str(start),
        end=str(end + pd.Timedelta(days=1)),
        auto_adjust=True,
        progress=False,
        threads=True
    )

    if raw.empty:
        return pd.DataFrame()

    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            prices = raw["Close"]
        else:
            return pd.DataFrame()
    else:
        if "Close" not in raw.columns:
            return pd.DataFrame()
        prices = raw[["Close"]].rename(
            columns={"Close": tickers[0]}
        )

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    prices.columns = [str(c) for c in prices.columns]

    prices = prices.dropna(how="all").sort_index()

    return prices

with st.spinner("Fetching stock market data..."):
    prices = download_data(tuple(tickers), start_date, end_date)

if prices.empty:
    st.error("No data received. Check your internet connection and try again.")
    st.stop()

prices = prices.ffill().dropna(how="all")
tickers = list(prices.columns)

if len(prices) < 2:
    st.error("Not enough historical data. Select a longer date range.")
    st.stop()

returns = prices.pct_change(fill_method=None).replace(
    [np.inf, -np.inf], np.nan
).dropna(how="all")

if returns.empty:
    st.error("Unable to calculate returns from the downloaded data.")
    st.stop()

# PORTFOLIO SETTINGS
st.sidebar.divider()
st.sidebar.subheader("Portfolio allocation")

equal_weights = st.sidebar.checkbox(
    "Use equal stock weights",
    value=True
)

if equal_weights:
    weights = pd.Series(1 / len(tickers), index=tickers)
else:
    weight_values = {}

    for ticker in tickers:
        weight_values[ticker] = st.sidebar.number_input(
            f"{ticker} allocation (%)",
            min_value=0.0,
            max_value=100.0,
            value=round(100 / len(tickers), 2),
            step=5.0,
            key=f"weight_{ticker}"
        )

    total_weight = sum(weight_values.values())

    if total_weight <= 0:
        st.warning("Set at least one stock allocation above zero.")
        st.stop()

    weights = pd.Series({
        ticker: value / total_weight
        for ticker, value in weight_values.items()
    })

# CALCULATIONS
portfolio_returns = (
    returns[weights.index]
    .fillna(0)
    .mul(weights, axis=1)
    .sum(axis=1)
)

portfolio_value = investment * (
    1 + portfolio_returns
).cumprod()

normalized_prices = prices.div(prices.iloc[0]) * 100

cumulative_returns = (
    (1 + returns.fillna(0)).cumprod() - 1
) * 100

volatility = returns.std() * np.sqrt(252) * 100

drawdowns = prices.div(prices.cummax()).sub(1) * 100

max_drawdown = drawdowns.min()

historical_var = -returns.quantile(0.05) * 100

total_return = (
    portfolio_value.iloc[-1] / investment - 1
) * 100

portfolio_volatility = (
    portfolio_returns.std() * np.sqrt(252) * 100
)

portfolio_drawdown = (
    portfolio_value / portfolio_value.cummax() - 1
).min() * 100

# KEY METRICS
st.caption(
    f"Data from {prices.index.min().date()} "
    f"to {prices.index.max().date()} · "
    f"{len(prices):,} trading observations"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Portfolio Value",
    f"${portfolio_value.iloc[-1]:,.2f}"
)

c2.metric(
    "Total Return",
    f"{total_return:.2f}%"
)

c3.metric(
    "Annualized Volatility",
    f"{portfolio_volatility:.2f}%"
)

c4.metric(
    "Maximum Drawdown",
    f"{portfolio_drawdown:.2f}%"
)

# DASHBOARD TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Performance",
    "Risk Analysis",
    "Portfolio Simulator",
    "Monte Carlo",
    "Data & Reports"
])

# TAB 1: OVERVIEW
with tab1:
    st.subheader("Historical Stock Prices")

    fig = go.Figure()

    for ticker in tickers:
        fig.add_trace(go.Scatter(
            x=prices.index,
            y=prices[ticker],
            mode="lines",
            name=ticker
        ))

    fig.update_layout(
        template="plotly_dark",
        height=500,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Adjusted Price (USD)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Comparing Stock Growth")

    fig = px.line(
        normalized_prices,
        labels={
            "value": "Growth of $100",
            "index": "Date",
            "variable": "Stock"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Stock Summary")

    summary = pd.DataFrame({
        "Latest Price ($)": prices.iloc[-1],
        "Period Return (%)": (
            prices.iloc[-1] / prices.iloc[0] - 1
        ) * 100,
        "Annualized Volatility (%)": volatility,
        "Maximum Drawdown (%)": max_drawdown,
        "Historical VaR 95% (%)": historical_var
    })

    st.dataframe(summary.round(2), use_container_width=True)

# TAB 2: PERFORMANCE
with tab2:
    st.subheader("Cumulative Returns")

    fig = px.line(
        cumulative_returns,
        labels={
            "value": "Return (%)",
            "index": "Date",
            "variable": "Stock"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Returns")

    fig = px.line(
        returns * 100,
        labels={
            "value": "Daily Return (%)",
            "index": "Date",
            "variable": "Stock"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    selected_stock = st.selectbox(
        "Choose a stock for moving averages",
        tickers
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=prices.index,
        y=prices[selected_stock],
        name="Stock Price"
    ))

    fig.add_trace(go.Scatter(
        x=prices.index,
        y=prices[selected_stock].rolling(20).mean(),
        name="20-Day Average"
    ))

    fig.add_trace(go.Scatter(
        x=prices.index,
        y=prices[selected_stock].rolling(50).mean(),
        name="50-Day Average"
    ))

    fig.update_layout(
        title=f"{selected_stock} Moving Averages",
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# TAB 3: RISK ANALYSIS
with tab3:
    st.subheader("Risk Metrics")

    risk_table = pd.DataFrame({
        "Annualized Volatility (%)": volatility,
        "Maximum Drawdown (%)": max_drawdown,
        "Historical VaR 95% (%)": historical_var,
        "Average Daily Return (%)": returns.mean() * 100
    })

    st.dataframe(risk_table.round(3), use_container_width=True)

    st.subheader("Stock Correlation")

    correlation = returns.corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drawdown Over Time")

    fig = px.line(
        drawdowns,
        labels={
            "value": "Drawdown (%)",
            "index": "Date",
            "variable": "Stock"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Historical VaR estimates a loss threshold from past returns. "
        "It does not predict or cap future losses."
    )

# TAB 4: PORTFOLIO SIMULATOR
with tab4:
    st.subheader("Portfolio Allocation")

    st.dataframe(
        (weights * 100).rename(
            "Allocation (%)"
        ).to_frame().round(2),
        use_container_width=True
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=portfolio_value.index,
        y=portfolio_value,
        mode="lines",
        name="Portfolio Value"
    ))

    fig.add_hline(
        y=investment,
        line_dash="dash",
        annotation_text="Starting Investment"
    )

    fig.update_layout(
        title="Hypothetical Portfolio Growth",
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Value (USD)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Portfolio Performance")

    elapsed_years = max(
        (portfolio_value.index[-1] -
         portfolio_value.index[0]).days / 365.25,
        0
    )

    if elapsed_years > 0 and portfolio_value.iloc[-1] > 0:
        annualized_return = (
            (portfolio_value.iloc[-1] / investment)
            ** (1 / elapsed_years) - 1
        ) * 100
    else:
        annualized_return = np.nan

    daily_std = portfolio_returns.std()

    sharpe = (
        portfolio_returns.mean() * 252 /
        (daily_std * np.sqrt(252))
        if daily_std > 0 else np.nan
    )

    metrics = pd.DataFrame({
        "Metric": [
            "Starting Investment ($)",
            "Latest Portfolio Value ($)",
            "Total Return (%)",
            "Annualized Return (%)",
            "Annualized Volatility (%)",
            "Sharpe Ratio (0% risk-free rate)",
            "Maximum Drawdown (%)"
        ],
        "Value": [
            investment,
            portfolio_value.iloc[-1],
            total_return,
            annualized_return,
            portfolio_volatility,
            sharpe,
            portfolio_drawdown
        ]
    })

    st.dataframe(metrics.round(3), use_container_width=True)

    st.caption(
        "This is a hypothetical historical simulation, "
        "not a recommendation to buy or sell stocks."
    )

# TAB 5: MONTE CARLO
with tab5:
    st.subheader("Monte Carlo Simulation")

    number_of_simulations = st.slider(
        "Number of simulated paths",
        min_value=100,
        max_value=2000,
        value=500,
        step=100
    )

    forecast_days = st.slider(
        "Trading days into the future",
        min_value=21,
        max_value=252,
        value=252,
        step=21
    )

    if portfolio_returns.std() == 0:
        st.warning("Not enough variation in returns to simulate scenarios.")
    else:
        rng = np.random.default_rng(42)

        simulated_returns = rng.normal(
            portfolio_returns.mean(),
            portfolio_returns.std(),
            size=(forecast_days, number_of_simulations)
        )

        simulated_values = investment * np.cumprod(
            1 + simulated_returns,
            axis=0
        )

        future_dates = pd.bdate_range(
            start=prices.index[-1] + pd.Timedelta(days=1),
            periods=forecast_days
        )

        simulation_df = pd.DataFrame(
            simulated_values,
            index=future_dates
        )

        fig = go.Figure()

        for i in range(min(50, number_of_simulations)):
            fig.add_trace(go.Scatter(
                x=simulation_df.index,
                y=simulation_df.iloc[:, i],
                mode="lines",
                line={"width": 1},
                opacity=0.3,
                showlegend=False
            ))

        fig.update_layout(
            title="Simulated Portfolio Scenarios",
            template="plotly_dark",
            height=450,
            xaxis_title="Future Date",
            yaxis_title="Portfolio Value ($)"
        )

        st.plotly_chart(fig, use_container_width=True)

        final_values = simulation_df.iloc[-1]

        p5 = final_values.quantile(0.05)
        median = final_values.median()
        p95 = final_values.quantile(0.95)

        a, b, c = st.columns(3)

        a.metric("5th Percentile", f"${p5:,.2f}")
        b.metric("Median Scenario", f"${median:,.2f}")
        c.metric("95th Percentile", f"${p95:,.2f}")

        probability_loss = (
            final_values < investment
        ).mean() * 100

        st.metric(
            "Simulated chance of ending below starting value",
            f"{probability_loss:.2f}%"
        )

        fig = px.histogram(
            final_values,
            nbins=40,
            title="Distribution of Final Simulated Values"
        )

        fig.add_vline(
            x=investment,
            line_dash="dash",
            annotation_text="Starting Investment"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "These are illustrative scenarios using a simplified "
            "normal-return assumption, not predictions."
        )

# TAB 6: DATA AND REPORTS
with tab6:
    st.subheader("Historical Prices")
    st.dataframe(prices.tail(100), use_container_width=True)

    st.subheader("Download Reports")

    def csv_bytes(frame):
        return frame.to_csv().encode("utf-8")

    st.download_button(
        "Download Historical Prices CSV",
        csv_bytes(prices),
        "historical_prices.csv",
        "text/csv"
    )

    st.download_button(
        "Download Daily Returns CSV",
        csv_bytes(returns),
        "daily_returns.csv",
        "text/csv"
    )

    st.download_button(
        "Download Performance Summary CSV",
        csv_bytes(summary),
        "performance_summary.csv",
        "text/csv"
    )

    st.download_button(
        "Download Portfolio Growth CSV",
        csv_bytes(
            portfolio_value.rename(
                "Portfolio Value"
            ).to_frame()
        ),
        "portfolio_growth.csv",
        "text/csv"
    )

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        prices.to_excel(writer, sheet_name="Prices")
        returns.to_excel(writer, sheet_name="Daily Returns")
        summary.to_excel(writer, sheet_name="Performance")
        risk_table.to_excel(writer, sheet_name="Risk")
        (weights * 100).rename(
            "Allocation (%)"
        ).to_frame().to_excel(writer, sheet_name="Weights")
        portfolio_value.rename(
            "Portfolio Value"
        ).to_frame().to_excel(writer, sheet_name="Portfolio")

    st.download_button(
        "Download Complete Excel Report",
        excel_buffer.getvalue(),
        "TechStock_Insights_Report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()
st.caption(
    "TechStock Insights · Educational analytics project · "
    "Data from Yahoo Finance · Not financial advice."
)