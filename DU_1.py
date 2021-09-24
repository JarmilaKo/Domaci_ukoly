import pandas as pd
import requests
import numpy as np

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
open("london_merged.csv", 'wb').write(r.content)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/tested.csv")
open("tested.csv", 'wb').write(r.content)

df_tested = pd.read_csv("tested.csv")
# print(df_tested.tail(10))

df_tested_pivot = df_tested.pivot_table(values="Survived",
                                        columns="Pclass",
                                        index="Sex",
                                        aggfunc=len,
                                        margins=True)
print(df_tested_pivot)
print("Dekuji, Rado")
london_merged = pd.read_csv("london_merged.csv")
london_merged["timestamp"] = pd.to_datetime(london_merged["timestamp"])
london_merged["year"] = london_merged["timestamp"].dt.year
london_merged_pivot = london_merged.pivot_table(values="cnt",
                                                columns="weather_code",
                                                index="year",
                                                aggfunc=np.count_nonzero,
                                                margins=True)
london_merged_pivot_percentage = london_merged_pivot.div(london_merged_pivot.iloc[:, -1], axis=0)

print(london_merged_pivot_percentage)


