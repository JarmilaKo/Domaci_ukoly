import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statistics

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

crypto = pd.read_csv("crypto_prices.csv")
crypto["pct_change"] = crypto.groupby("Name")["Close"].pct_change()
crypto["pct_change"] = crypto["pct_change"] + 1

XMR = crypto[crypto["Symbol"] == "XMR"]["pct_change"].dropna(axis="rows")
XMR = XMR.tolist()
print(f"Geometrický prumer XMR je {statistics.geometric_mean(XMR) - 1}")

# Neumím vypočítat geometrický průměr přes apply.
symbols = crypto["Symbol"].unique()
for symbol in symbols:
    sestava = crypto[crypto["Symbol"] == symbol]["pct_change"].dropna(axis="rows")
    sestava = sestava.tolist()
    print(f"Geometrický průměr pro {symbol} je {statistics.geometric_mean(sestava) - 1}.")
