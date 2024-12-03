import requests
from loguru import logger as lg
from config.response_arg import cookies, headers

def get_request(amount = 20, interval = 1, name = "SBER"):
  params = {
        'callback': 'jQuery111204316999394961374_1720869957586',
        'iss.meta': 'on',
        's1.type': 'candles',
        'interval': interval,
        'candles': amount,
        'indicators': ''
  }

  response = requests.get(
        f'https://iss.moex.com/cs/engines/stock/markets/shares/boardgroups/57/securities/{name}.hs',
        params=params,
        cookies=cookies,
        headers=headers,
  )

  if response.status_code == 200:
      print(response.text)
      return response
  
  lg.warning(f"Something went wrong with code {response.status_code}")
  return None