import requests
import pandas as pd
from scipy.stats import mannwhitneyu

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

air_polution = pd.read_csv("air_polution_ukol.csv")
air_polution["date"] = pd.to_datetime(air_polution["date"], format="%Y/%m/%d")
air_polution["month"] = air_polution["date"].dt.month
air_polution["year"] = air_polution["date"].dt.year
print(air_polution.head())
air_pol_leden_19 = air_polution[(air_polution["month"] == 1) & (air_polution["year"] == 2019)]["pm25"]
air_pol_leden_20 = air_polution[(air_polution["month"] == 1) & (air_polution["year"] == 2020)]["pm25"]

# Nulová hypotéza je, že množství jemných částic bylo stejné. Alternativní je, že se množství částic lišilo.
print(mannwhitneyu(air_pol_leden_19, air_pol_leden_20))
# pvalue vychází 1,1%, je tedy nižší než hladina významnosti a tudíž zamítáme nulovou hypotézu a přikláníme se k
# hypotéze, že množství jemných částic se v lednu 2020 oproti lednu 2019 lišilo. Pravděpodobnost, že pozorovaný
# rozdíl v hodnotách je dán náhodou, je cca 1,1%.
