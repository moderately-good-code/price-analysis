#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 11:11:37 2022

@author: moderately-good-code
"""

import pandas as pd
import asset

def save_df_as_parquet(df: pd.DataFrame) -> None:
    filename = asset.TS_FILE_DIR + df.loc[0].at["symbol"] + ".parquet"
    print(f"Changing file {filename} ...", end="")
    df.to_parquet(filename, engine="fastparquet")
    print(" done!")

def load_df_from_parquet(asset_name: str) -> pd.DataFrame:
    filename = asset.TS_FILE_DIR + asset_name + ".parquet"
    print(f"Loading file {filename}...", end="")
    df = pd.read_parquet(filename, engine="fastparquet")
    print(" done!")
    return df

def join_dfs(old_df: pd.DataFrame, new_df: pd.DataFrame):
    pass # TODO