import pandas as pd
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
    open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

air_polution = pd.read_csv("air_polution_ukol.csv")
air_polution["date"] = pd.to_datetime(air_polution["date"], format="%Y/%m/%d")
air_polution["month"] = air_polution["date"].dt.month
air_polution["year"] = air_polution["date"].dt.year

air_polution_pivot = pd.pivot_table(air_polution,
                                    values="pm25",
                                    columns="month",
                                    index="year",
                                    aggfunc=np.mean,
                                    margins=True)
print("Kontingenční tabulka porovnávající znečištění po měsících a letech: ")
print(air_polution_pivot)

sns.heatmap(air_polution_pivot, annot=True, cmap="YlGn")
plt.show()

air_polution["den_v_tydnu"] = air_polution["date"].dt.dayofweek
air_polution["typ_dne"] = np.where(air_polution["den_v_tydnu"] < 5, "pracovni_den", "vikend")
print("Průměrné hodnoty znečištění v pracovní dny a o víkendech: ")
print(air_polution.groupby("typ_dne")["pm25"].mean())
print("\n")
# Níže je kontrola správnosti výpočtu průměrných hodnot znečištění v pracovní dny a o víkendech.

air_polution_pivot2 = pd.pivot_table(air_polution,
                                     values="pm25",
                                     index="typ_dne",
                                     columns="year",
                                     aggfunc = np.mean,
                                     margins=True)
print(air_polution_pivot2)
