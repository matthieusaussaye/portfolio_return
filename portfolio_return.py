import numpy
import pandas as pd
import plotly
import math
from pandas_datareader import data as wb

def simple_return(col) :
    """
    Compute simple daily return for a given column
    """
    return((col/col.shift(1))-1)

def cumulative_perc(col) :
    """
    Compute cumulative percentage for a given column
    """
    return(simple_return(col).expanding(min_periods=2).sum()*100)

def portfolio_dataframe(tickers) : 

    """
    Compute the entire portfolio dataframe with cumulative percentages for each columns
    """

    new_data = pd.DataFrame()
    for t in tickers :
        new_data[t] = wb.DataReader(t, data_source='yahoo', start='2021-1-1')['Adj Close']
    for t in tickers :
        new_data[f'cumulative_perc_{t}'] = cumulative_perc(new_data[t])

    new_data['portfolio_cumulative_perc'] = new_data[[f'cumulative_perc_{t}' for t in tickers]].sum(axis=1)
    new_data['portfolio_cumulative_perc'] = new_data['portfolio_cumulative_perc']/len(tickers)

    cols = ['portfolio_cumulative_perc']
    for t in tickers :
        cols.append(f'cumulative_perc_{t}')
    return new_data[cols]

