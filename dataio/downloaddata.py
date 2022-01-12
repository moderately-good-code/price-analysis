#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 08:31:11 2022

@author: moderately-good-code
"""

# import pandas_datareader as pdr
import numpy as np
# import csv
import requests
from datetime import datetime
import pytz

import pandas as pd

import asset

# TODO: clean up

# TODO: documentation

def get_data_alphavantage(asset_name: str, api_key: str, interval: str="60min",
                          timeslice: str=None) -> pd.DataFrame:
    # TODO: check validity of arguments
    if interval != "daily":
        raise NotImplementedError("only daily interval implemented so far")
    
    # create URL
    if interval == "daily":
        av_function = "TIME_SERIES_DAILY"
    elif interval in ["60min"] and not timeslice:
        av_function = "TIME_SERIES_INTRADAY"
    elif interval in ["60min"] and timeslice:
        av_function = "TIME_SERIES_INTRADAY_EXTENDED"
    data_url = f"https://www.alphavantage.co/query?function={av_function}"
    data_url += f"&symbol={asset_name}"
    if interval != "daily":
        data_url += f"&interval={interval}"
    if timeslice:
        data_url += f"&slice={timeslice}"
    data_url += f"&apikey={api_key}"
    
    # download CSV
    with requests.Session() as s:
        download = s.get(data_url)
        # decoded_content = download.content.decode('utf-8')
    
    # parse data to dict with numpy arrays
    res = {"symbol": asset_name, "open": [], "close": [], "low": [],
           "high": [], "volume": [], "dates": []}
    if interval == "daily":
        # daily data is downloaded as json
        data = download.json()
        
        # get meta data
        res["last refreshed"] = data["Meta Data"]["3. Last Refreshed"]
        res["timezone"] = data["Meta Data"]["5. Time Zone"]
        
        # get time series data
        for day, data_point in data["Time Series (Daily)"].items():
             res["open"].append(data_point["1. open"])
             res["high"].append(data_point["2. high"])
             res["low"].append(data_point["3. low"])
             res["close"].append(data_point["4. close"])
             res["volume"].append(data_point["5. volume"])
             res["dates"].append(day)
    
    # convert to numpy dicts
    for key in ["open", "close", "low", "high", "volume"]:
        res[key] = np.array(res[key])
        
    # TODO: define order (newest first?)
    
    # convert timezones
    old_timezone = pytz.timezone(res["timezone"])
    new_timezone = pytz.timezone(asset.LOCAL_TIMEZONE)
    if interval == "daily":
        av_datetime_format = "%Y-%m-%d"
    else:
        av_datetime_format = "%Y-%m-%d %H:%M:%S"
    for i in range(len(res["dates"])):
        dt = datetime.strptime(res["dates"][i], av_datetime_format)
        res["dates"][i] = old_timezone.localize(dt).astimezone(new_timezone).strftime(asset.DATETIME_FORMAT)
    res["timezone"] = asset.LOCAL_TIMEZONE
    
    return pd.DataFrame.from_dict(res)
