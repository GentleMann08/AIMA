import asyncio
import pandas as pd
import json
from loguru import logger as lg
from get_request import get_request

async def get_data(name="SBER"):
    dump = []
    vol = []
    all_data = await get_request(amount=30000, name=name)

    if all_data is None:
        lg.error(f"No data fetched for {name}.")
        return None
    else:
        lg.info(f"Data for {name} loaded successfully.")
    
    try:
        all_data = json.loads(all_data[all_data.find("{"):all_data.rfind("}")+1])
        for index in all_data['candles']:
            for data in index['data'][::-1]:
                dump.append(data)
        for index in all_data['volumes']:
            for data in index['data'][::-1]:
                vol.append(data)
        
        df = pd.DataFrame(dump, columns=['Date', 'Open', 'Max', 'Min', 'Close'])
        df['Vol'] = 0.0

        for data in vol:
            df.loc[df["Date"] == data[0], "Vol"] = data[1]

        return df
    except Exception as e:
        lg.error(f"Error processing data for {name}. Error: {str(e)}")
        return None