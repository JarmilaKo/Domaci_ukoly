import pandas as pd
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
open("london_merged.csv", 'wb').write(r.content)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/titanic.csv")
open("titanic.csv", 'wb').write(r.content)

df_titanic = pd.read_csv("titanic.csv")
# print(df_titanic.tail(10))

df_titanic_pivot = df_titanic.pivot_table(values="Name",
                                          columns="Pclass",
                                          index=("Sex", "Survived"),
                                          aggfunc=len,
                                          margins=True)
print("\n")
print("Kontingenční tabulka s počtem přeživších a mrtvých dle třídy a pohlaví: ")
print(df_titanic_pivot)
print("\n")

df_titanic_pivot2 = df_titanic.pivot_table(values="Survived",
                                           columns="Pclass",
                                           index="Sex",
                                           aggfunc=np.mean,
                                           margins=True)
print("Kontingenční tabulka relativní míry přežití dle třídy a pohlaví: ")
print(df_titanic_pivot2)
print("\n")

# MOHU NEJAK SPECIFIKOVAT POČET DESETINNYCH MIST VE VYSTUPNI KONTINGECNI TABULCE? IDEALNE BYCH CHTELA VÝSTUP ZOBRAZIT JAKO PROCENTA. :-)

df_titanic_1class = df_titanic[df_titanic["Pclass"] == 1]
df_titanic_1class = df_titanic_1class[["Age", "Survived", "Pclass", "Sex"]]
df_titanic_1class: DataFrame = pd.DataFrame(df_titanic_1class)
labels = ["dite", "pubertak", "dospely", "senior"]
df_titanic_1class["age_group"] = pd.cut(df_titanic_1class["Age"], bins=[0, 12, 18, 60, 100], labels=labels)

df_titanic_1class_pivot = df_titanic_1class.pivot_table(values="Survived",
                                                        columns="age_group",
                                                        index="Sex",
                                                        aggfunc=np.mean,
                                                        margins=True)
print("Kontingenční tabulka relativní míry přežití cestujících v první třídě dle věkové skupiny a pohlaví: ")
print(df_titanic_1class_pivot)
print("\n")
# sns.heatmap(df_titanic_pivot, annot=True, fmt=".1f", cmap="YlGn")
# plt.show()

london_merged = pd.read_csv("london_merged.csv")
london_merged["timestamp"] = pd.to_datetime(london_merged["timestamp"])
london_merged["year"] = london_merged["timestamp"].dt.year
london_merged_pivot = london_merged.pivot_table(values="cnt",
                                                columns="weather_code",
                                                index="year",
                                                aggfunc=np.count_nonzero,
                                                margins=True)
print("Kontingenční tabulka s počtem jízd dle kódu počasí a roku: ")
print(london_merged_pivot)
print("\n")

london_merged_pivot_percentage = london_merged_pivot.div(london_merged_pivot.iloc[:, -1], axis=0)
print("Kontingeční tabulka s relativní mírou jízd v jednotlivých letech dle kódu počasí:")
print(london_merged_pivot_percentage)

sns.heatmap(london_merged_pivot_percentage, annot=True, fmt=".2f", cmap="YlGn")
plt.show()


