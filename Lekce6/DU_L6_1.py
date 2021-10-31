import requests
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/psenice.csv") as r:
  open("psenice.csv", 'w', encoding="utf-8").write(r.text)

psenice = pd.read_csv("psenice.csv")
print(psenice.head())
psenice.plot()
# plt.show()

# Nulová hypotéza je, že velikost zrn je stejná. Alternativní je, že se velikost liší.
rosa = psenice["Rosa"]
canadian = psenice["Canadian"]
print(mannwhitneyu(rosa, canadian))

# pvalue vyšla 3.522437521029982e-24 tedy hluboko pod hladinou významnosti 0,05 a tudíž můžeme zamítnout nulovou hypotézu, že by zrna
# měla stejnou velikost. pvalue říká pravděpodobnost, se kterou jsou rozdíly v datech výsledkem náhody. Ta nám vyšla
# pod 5%, tedy je menší 5% pravděpodobnost, že rozdíl v datech je dán náhodou.

