# Equity Asset Selection Framework

This Python script serves as a framework for selecting the best four equity-based assets from a specified basket. The selection is based on volatility and triple-momentum factors. The script utilizes the Yahoo Finance API (`yfinance`), `pandas`, and `talib` libraries for data retrieval, manipulation, and technical analysis.

## Features
- **Data Retrieval:** Historical data for a given list of ETF symbols is fetched from Yahoo Finance.
- **Momentum Calculation:** The script calculates the momentum factor using a weighted average of percentage changes over different time periods.
- **RSI Calculation:** Relative Strength Index (RSI) is calculated for each ETF.
- **Ranking:** ETFs are ranked based on momentum and RSI factors, and the top four are selected.
- **Weight Determination:** Weights are assigned to the selected ETFs based on their ranks and specific conditions.

## Parameters
- `etf_symbols`: List of ETF symbols from different regions.
- `G_ETFFILTER`: Number of top-ranked ETFs to filter.
- `G_MOM1`, `G_MOM2`, `G_MOM3`, `G_MOM4`: Parameters for momentum calculation.

## Functions
1. **fetch_data(symbol):**
   - Fetches historical data for a given symbol.

2. **calculate_momentum(data):**
   - Calculates the momentum factor using a weighted average.

3. **calculate_rsi(data):**
   - Calculates the Relative Strength Index (RSI).

4. **check_and_replace(rank_df_in):**
   - Checks and replaces occurrences in the first four lines of a DataFrame.

5. **rank_etfs(etf_data):**
   - Ranks ETFs based on momentum and RSI factors.

6. **determine_weights(selected_etfs):**
   - Determines weights for selected ETFs based on specific conditions.

## Usage
The script is set up to work with a predefined list of ETF symbols. You can customize the script by modifying the `etf_symbols` list or adjusting the parameters for momentum calculation.

```python
# Example usage
etf_data = pd.DataFrame()

for symbol in etf_symbols:
    data = fetch_data(symbol)
    etf_data[symbol] = data
    etf_data[symbol+'_Mom'] = calculate_momentum(etf_data[symbol])
    etf_data[symbol+'_RSI'] = calculate_rsi(etf_data[symbol])

selected_etfs = rank_etfs(etf_data)
weights = determine_weights(selected_etfs)
print(selected_etfs)
print(weights)
```

Feel free to adapt the script to suit your specific requirements or extend its functionality as needed.
