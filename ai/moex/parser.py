import pandas as pd
import aiohttp
import asyncio
from matplotlib import pyplot as plt
from datetime import datetime

async def fetch_stock_data(security, start_date, end_date, interval):
    url = f"http://iss.moex.com/iss/engines/stock/markets/shares/securities/{security}/candles.json"
    params = {
        "from": start_date,
        "till": end_date,
        "interval": interval
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Ошибка {response.status}: Не удалось получить данные.")
            return await response.json()

async def save_and_plot_stock_data(security, start_date, end_date, interval, csv_path, image_path):
    try:
        data = await fetch_stock_data(security, start_date, end_date, interval)
        if "candles" not in data or "data" not in data["candles"]:
            raise Exception("Данные отсутствуют или формат ответа изменился.")
        columns = data['candles']['columns']
        rows = data['candles']['data']
        if not rows:
            raise Exception("Нет данных для указанного интервала.")
        frame = pd.DataFrame([{k: r[i] for i, k in enumerate(columns)} for r in rows])
        frame['datetime'] = pd.to_datetime(frame['begin'])
        frame.set_index('datetime', inplace=True)
        frame.drop(columns=['begin'], inplace=True)
        frame.to_csv(csv_path, index=True)
        plt.figure(figsize=(10, 6))
        plt.plot(frame['close'], label="Closing Price")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title(f"Stock Prices for {security}")
        plt.legend()
        plt.grid()
        plt.savefig(image_path)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

async def main(security='VEON-RX'):
    await save_and_plot_stock_data(
        security=security,
        start_date="2024-01-01",
        end_date=datetime.today().strftime('%Y-%m-%d'),
        interval=24,
        csv_path=f"data/{security}.csv",
        image_path=f"plots/{security}.png"
    )

asyncio.run(main())