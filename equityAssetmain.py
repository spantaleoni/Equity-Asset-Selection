#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:26:43 2023

@author: simonlesflex
"""

import yfinance as yf
import pandas as pd
import talib

# List of ETF symbols from different regions
etf_symbols = ['QQQ', 'FEZ', 'RSP', 'IWM', 'SPY', 'NFTY', 'FTXL', 'IWY', 'EWJ', 'EWZ', 'CQQQ', 'EWA', 'URTH']
G_ETFFILTER = 4
G_MOM1 = 21
G_MOM2 = 63
G_MOM3 = 128
G_MOM4 = 252

# Function to fetch historical data for a given symbol
def fetch_data(symbol):
    data = yf.download(symbol, start='2021-01-01', end='2023-01-01')
    return data['Adj Close']

# Function to calculate momentum factor
def calculate_momentum(data):
    momDF = data
    momDF = (((12* momDF.pct_change(G_MOM1)) + (4* momDF.pct_change(G_MOM2)) + (2* momDF.pct_change(G_MOM3))) / 3) + (8* momDF.rolling(45).std())
    return momDF

# Function to calculate RSI
def calculate_rsi(data):
    return talib.RSI(data, timeperiod=G_MOM3)


# Function to check and replace occurrences in the first 4 lines
def check_and_replace(rank_df_in):
    symbols_to_check = ['SPY_totR', 'RSP_totR', 'QQQ_totR']
    occurrences_count = 0
    df = rank_df_in
    
    for index, row in df.iterrows():
        symbol = row['Symbol']
        if symbol in symbols_to_check:
            occurrences_count += 1
            if occurrences_count > 1:
                # Replace with the following entry in the DataFrame lines
                df = df.drop([index])

    return df


# Function to rank ETFs based on momentum and RSI factors
def rank_etfs(etf_data):
    momentum_rank = etf_data.filter(like='_Mom').rank(ascending=False, axis=1).fillna(0)
    rsi_rank = etf_data.filter(like='_RSI').rank(ascending=True, axis=1).fillna(0)  # Note: ascending=True for RSI ranking
    
    # Create separate total rank columns for each ETF
    for symbol in etf_symbols:
        etf_data[f'{symbol}_totR'] = (momentum_rank[symbol+'_Mom'] + rsi_rank[symbol+'_RSI']) / 2

    # Extract the last row of the DataFrame
    last_row = etf_data.iloc[-1]
    # Filter only columns containing '_totR'
    totR_columns = last_row.filter(like='_totR')
    # Create a new DataFrame with symbols and their corresponding total rank values
    rank_df = pd.DataFrame({'Symbol': totR_columns.index, 'Total_Rank': totR_columns.values})
    # Sort the DataFrame in descending order based on the Total_Rank column
    rank_df = rank_df.sort_values(by='Total_Rank', ascending=False)
    # Example usage with your provided DataFrame
    rank_df = pd.DataFrame({
    'Symbol': ['NFTY_totR', 'RSP_totR', 'IWM_totR', 'SPY_totR', 'EWZ_totR', 'IWY_totR', 'QQQ_totR', 'URTH_totR', 'FEZ_totR', 'EWA_totR', 'FTXL_totR', 'EWJ_totR', 'CQQQ_totR'],
    'Total_Rank': [11.0, 9.0, 8.5, 8.5, 8.5, 8.0, 7.5, 7.5, 6.5, 6.5, 5.0, 3.5, 1.0] })
    updated_rank_df = check_and_replace(rank_df)
    
    return updated_rank_df.head(G_ETFFILTER)


def determine_weights(selected_etfs):
    weights = [0.25] * len(selected_etfs)  # Default weight is 25%

    qqq_position = selected_etfs['Symbol'].iloc[0]  # Get the symbol of the first row (highest Total_Rank)

    if qqq_position == 'QQQ_totR':
        weights = [1] + [0] * (len(selected_etfs) - 1)  # 100% weight for QQQ_totR, 0% for others
    elif qqq_position == 'NFTY_totR':
        weights[0] = 0.5  # Assign 50% weight to NFTY_totR
        weights[1] = .5 / 3
        weights[2] = .5 / 3
        weights[3] = .5 / 3

    weight_df = pd.DataFrame({'Symbol': selected_etfs['Symbol'], 'Weight': weights})
    return weight_df

# Main script
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

# Output DataFrame with selected ETFs and weights
#output_df = pd.DataFrame({'ETF': selected_etfs.columns, 'Weight': weights})
#print(output_df)
