from loguru import logger as lg
import json
from tqdm import tqdm 
import pandas as pd
from get_request import get_request

def get_jquery(amount = 20000, interval = 1, name = "SBER"):
    lg.debug("Sending request to MOEX")
    response = get_request(amount, interval, name)
    lg.debug("GOT RESPONSE")
    if response == None:
      raise ValueError("Too many data")
    answer = str(response.content)
    while answer[0] != "{":
        answer = answer[1:]
    return json.loads(answer[:-3])

def get_data(name = "SBER"):
    dump = []
    vol = []
    all_data = get_jquery(amount = 30000, name = name)
    if all_data == None:
      lg.error("BAD GUY")
    else:
      lg.info("Data was loaded successfully")
      for index in all_data['candles']:
        all = 0
        for data in index['data'][::-1]:
          dump.append(data)
          all += 1
        for index in all_data['volumes']:
            all = 0
            for data in index['data'][::-1]:
              vol.append(data)
              all += 1
    df = pd.DataFrame(dump, columns=['Date', 'Open', 'Max', 'Min', 'Close'])
    
    df['Vol'] = [0.0]*df.shape[0]
    
    for data in tqdm(vol):
      df.loc[df["Date"] == data[0], "Vol"] = data[1]
      
    return df