import requests
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Fish.csv")
with open("Fish.csv", "wb") as f:
    f.write(r.content)

fish = pd.read_csv("Fish.csv")

avg_weight_by_species = fish.groupby("Species")["Weight"].mean()
fish["avg_species_weight"] = fish["Species"].map(avg_weight_by_species)
print(fish.corr())

mod = smf.ols(formula="Weight ~ Length2 + Height + avg_species_weight", data=fish)
res = mod.fit()
print(res.summary())

# fig, (ax1, ax2) = plt.subplots(1, 2)
# fish.plot.scatter(x="Weight", y="avg_species_weight", ax=ax1)
# fish.plot.scatter(x="Length2", y="avg_species_weight", ax=ax2)

species = pd.Series(fish["Species"].unique(), name="Species")
species = species.to_frame()
colors = pd.DataFrame(["red", "green", "orange", "blue", "yellow", "black", "brown"], columns=["Color"])
species_colors = species.join(colors)
species_colors = fish.merge(species_colors, on="Species")

# Tento scatter nám ukazuje, že máme jeden druh ryby, který se liší v poměrech délky a váhy od ostatních.
# Moje hypotéza tedy je, že toto je důvod, proč přidání hodnoty průměrné váhy druhu ryby modelu pomáhá.
species_colors.plot.scatter(x="Length2", y="Weight", c="Color")
plt.show()
