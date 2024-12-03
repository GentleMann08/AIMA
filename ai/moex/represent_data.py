from matplotlib import pyplot as plt
from datetime import datetime
import seaborn as sns
from get_data import get_data

def _plot_series(series, series_name, series_index=0):
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = (series['Date']//1000).apply(datetime.utcfromtimestamp)
  ys = series['Close']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

def represent_data(name = "SBER"):
    df = get_data(name)
    if df is not None:
        print(name)
        print(df.head())
        fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
        df_sorted = df.sort_values('Date', ascending=True)
        _plot_series(df_sorted, '')
        sns.despine(fig=fig, ax=ax)
        plt.xlabel('Date')
        _ = plt.ylabel('Close')
        plt.title(name)
        plt.savefig(f"plots/{name}.png")
        df.to_csv(f"data/{name}.csv")
        plt.close('all') 

exchange_shares = ["SBER", "VTBR", "MTSS", "GAZP"]
for share in exchange_shares:
    represent_data(share)
        