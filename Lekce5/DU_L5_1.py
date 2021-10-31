import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

crypto = pd.read_csv("crypto_prices.csv")
crypto["pct_change"] = crypto.groupby("Name")["Close"].pct_change()
crypto["pct_change"] = crypto["pct_change"] + 1

# Omezení dat na cca 1 měsíc.
crypto["Date"] = pd.to_datetime(crypto["Date"])
date = datetime.datetime(2021, 6, 1)
# crypto = crypto[crypto["Date"] >= date]

crypto_pivot = pd.pivot_table(data=crypto, index="Date", columns="Symbol", values="Close", aggfunc=np.sum)
crypto_pivot_corr = crypto_pivot.corr()
# print(crypto_pivot.corr(method="spearman"))

# Pokus o nalezení nejmenší hodnoty.
crypto_pivot_corr = pd.DataFrame(crypto_pivot_corr)
crypto_pivot_corr = crypto_pivot_corr.abs()
# Porovnáním dvou níže uvedených selektů, zjistím, že nejnižší korelační koeficient má kombinace USDT a UNI.
print(crypto_pivot_corr.min())
print(crypto_pivot_corr.idxmin())

# Zkusím vynést graf pro variantu USDT a UNI. USDT je lineární a konstantní. To vysvětluje nízký korelační koeficient.
crypto_pivot[["USDT", "UNI"]].plot()
plt.show()
