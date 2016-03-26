import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_max_price(symbol):
    tb=pd.read_csv("daily/table_{}.csv".format(symbol),names=["date","sm1","open","high","low","close","volume"])
    return tb["close"].mean()

def plot_historical(symbol):
    df=pd.read_csv(symbol_to_path(symbol),
                   names=["date","sm1","open","high","low","close","volume"])
    print(df[["high","low"]].head())
    df[["high","low"]].plot()
    plt.show()

def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir,"table_{}.csv".format(str(symbol)))

def get_base_dataframe(dates):
    df1=pd.DataFrame(index=dates)
    dfSPY=pd.read_csv(symbol_to_path("spy"),
                      names=["date","sm1","open","high","low","close","volume"],
                      usecols=["date","close"],
                      index_col="date",
                      na_values=['nan'],
                      parse_dates=True)
    dfSPY=dfSPY.iloc[::-1]
    dfSPY=dfSPY.rename(columns={'close':'spy'})
    df1=df1.join(dfSPY,how='inner')
    return df1

def get_data(symbols,dates):
    df1=get_base_dataframe(dates)
    for symbol in symbols:
        df_temp=pd.read_csv(symbol_to_path(symbol),
                          names=["date","sm1","open","high","low","close","volume"],
                          usecols=["date","close"],
                          index_col="date",
                          na_values=['nan'],
                          parse_dates=True)
        df_temp = df_temp.rename(columns={'close':symbol})
        df1=df1.join(df_temp)
    return df1


def plot_selected(df,symbols,start,end):
    df1=df.ix[start:end,symbols]
    ax = df1.plot(title="Plot Selected", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def test_run():
    a = np.random.randint(0,10,size=(2,8))
    a=a.reshape(4,4)
    print(a.shape)
    print(a)
    print(a[0:2,0:3])
    a[0,:]=1
    a[:,1]=0
    a[1,0:3]=2
    print(a)
    mean = a.mean()
    print(mean)
    print(a*2.0)

def rolling_mean(df):
    ax = df['SPY'].plot(title="SPY rolling mean", label='SPY')
    rm_SPY= pd.rolling_mean(df['SPY'],window=20)
    rm_SPY.plot(label='Rolling Mean', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()

def plot_rolling(df,mean, upper_band,lower_band):
    ax = df['SPY'].plot(title="SPY rolling mean", label='SPY')
    mean.plot(label='Rolling Mean', ax=ax)
    upper_band.plot(label="Upper band", ax=ax)
    lower_band.plot(label="Lower band",ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()


def plot_data(df,title="Stock prices"):
    ax = df.plot(title=title, fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def get_rolling_mean(values, window):
    return pd.rolling_mean(values['SPY'],window=window)

def get_rolling_std(values,window):
    return pd.rolling_std(values['SPY'],window=window)

def get_bands(rolling_mean, rolling_std):
    return (rolling_mean+2*rolling_std, rolling_mean-2*rolling_std)

def compute_daily_returns(df):
    return (df / df.shift(1))-1

def compute_cumulative_returns(df):
    return df.div(df.ix[0].values,axis="columns")-1

if __name__ == "__main__":
    start='2009-01-01'
    end='2012-12-31'
    dates=pd.date_range(start,end)
    df1=get_data([],dates)
    # mean = get_rolling_mean(df1,20)
    # std = get_rolling_std(df1,20)
    # upper_band,lower_band = get_bands(mean,std)
    df_daily=compute_daily_returns(df1)
    df_cum=compute_cumulative_returns(df1)
    # plot_data(df1,title="Closing")
    # plot_data(df_daily,title="Daily Returns")
    # plot_data(df_cum,title="Cummulative Returns")
    mean= df_daily['spy'].mean()
    std= df_daily['spy'].std()
    print("MEAN: " , mean)
    print("STD: ", std)
    df_daily.hist()
    plt.axvline(mean,color='w',linestyle='dashed',linewidth=2)
    plt.axvline(-std,color='r',linestyle='dashed',linewidth=2)
    plt.axvline(std,color='r',linestyle='dashed',linewidth=2)
    plt.show()
    # rolling_mean(df1)
    # plot_rolling(df1,mean,upper_band,lower_band)


    # df1=get_data(['ibm','aapl','msft','csco','goog'],dates)
    # df2= df1 / df1.ix[0]
    # plot_selected(df2,['spy','ibm','aapl','msft','csco','goog'],start,end)
    # mean = df1.mean()
    # median = df1.median()
    # std = df1.std()
    # print("Mean: \n" , mean)
    # print("Median: \n", median)
    # print("STD: \n", std)