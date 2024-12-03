import asyncio
import os
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime
import aiofiles
from get_data import get_data

async def _plot_series(series, series_name, series_index=0):
    palette = list(sns.palettes.mpl_palette('Dark2'))
    xs = (series['Date'] // 1000).apply(datetime.utcfromtimestamp)
    ys = series['Close']
    plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

async def represent_data(name="SBER"):
    df = await get_data(name)

    if df is not None and not df.empty:
        print(f"Plotting data for {name}")
        print(df.head())

        fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
        df_sorted = df.sort_values('Date', ascending=True)
        await _plot_series(df_sorted, name)

        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        sns.despine(fig=fig, ax=ax)
        plt.xlabel('Date')
        plt.ylabel('Close')
        plt.title(f"{name} Stock Data")

        os.makedirs('plots', exist_ok=True)
        os.makedirs('data', exist_ok=True)

        plot_path = f"plots/{name}.png"
        csv_path = f"data/{name}.csv"

        plt.savefig(plot_path)
        async with aiofiles.open(csv_path, 'w') as f:
            await f.write(df.to_csv(index=False))

        plt.close(fig) 
    else:
        print(f"No data found for {name}")

async def main():
    exchange_shares = ["ROSN"]
    tasks = [represent_data(share) for share in exchange_shares]
    await asyncio.gather(*tasks)

asyncio.run(main())