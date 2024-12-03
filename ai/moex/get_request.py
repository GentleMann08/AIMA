import aiohttp
import asyncio
from loguru import logger as lg
from config.response_arg import cookies, headers

async def get_request(amount=20, interval=1, name="SBER"):
    params = {
        'callback': 'jQuery111204316999394961374_1720869957586',
        'iss.meta': 'on',
        's1.type': 'candles',
        'interval': interval,
        'candles': amount,
        'indicators': ''
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://iss.moex.com/cs/engines/stock/markets/shares/boardgroups/57/securities/{name}.hs',
                params=params,
                cookies=cookies,
                headers=headers,
                ssl=False  
            ) as response:
                if response.status == 200:
                    lg.info(f"Request to MOEX for {name} was successful")
                    return await response.text()
                else:
                    lg.warning(f"Request failed for {name} with status code {response.status}")
                    return None
    except Exception as e:
        lg.error(f"Request failed for {name}. Error: {str(e)}")
        return None
