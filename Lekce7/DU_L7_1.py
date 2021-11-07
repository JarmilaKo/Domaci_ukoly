import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import numpy as np
from scipy.stats import norm, lognorm, shapiro
from fitter import Fitter, get_common_distributions, get_distributions
import statsmodels.formula.api as smf
pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Concrete_Data_Yeh.csv")
with open("Concrete_Data_Yeh.csv", "wb") as f:
    f.write(r.content)

beton = pd.read_csv("Concrete_Data_Yeh.csv")
print(beton.corr())

# mod = smf.ols(formula="csMPa ~ cement + slag + flyash + water + superplasticizer + age + coarseaggregate +"
#                       "fineaggregate", data=beton)
mod = smf.ols(formula="csMPa ~ cement + slag + flyash + water + superplasticizer + age", data=beton)
res = mod.fit()
print(res.summary())
# Koeficient determinace vychází poměrně nízký a sice 0,614.
# Negativní vliv na kompresní tlak betonu má voda.

# test normality rozdělení dat
stat, p = shapiro(beton["csMPa"])
print('pvalue testu na normální rozdělení je %.3f' % (p))
if p > 0.05:
    print('Data mají normální rozdělení')
else:
    print('Data nemají normální rozdělení. Zamítáme nulovou hypotézu.')

# zkouším, jaká distribuce nejlépe odpovídá datům. Vyšlo "burr". V tomto bodě své zkoumání končím.
csMPa = beton["csMPa"].values
f = Fitter(csMPa, distributions=['gamma', 'lognorm', "beta", "burr", "norm"])
print(f.fit())
print(f.summary())
print(f.get_best(method='sumsquare_error'))

fig, axs = plt.subplots(2, 2, figsize=(20, 8))
seaborn.distplot(beton["csMPa"], fit=norm, ax=axs[0, 0]).set_title("Porovnání s normální distibucí")
# Zkouším použít diplot, ale bez úspěchu.
# seaborn.displot(data=beton, x="csMPa", kind="hist", ax=axs[0, 0], kde=True)
seaborn.distplot(beton["csMPa"], fit=lognorm, ax=axs[0, 1]).set_title("Porovnání s lognormální distribucí")
seaborn.distplot(np.log(beton["csMPa"]), fit=norm, ax=axs[1, 0]).set_title("Log transformovaná data")
beton.plot.scatter(x="csMPa", y="cement", title="Scatter", ax=axs[1, 1])
plt.show()
