import requests
import pandas as pd
import numpy as np

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
    open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

presidents = pd.read_csv("1976-2020-president.csv")
presidents = presidents.sort_values(["state", "year"], ascending=True)
presidents["rank"] = presidents.groupby(["state", "year"])["candidatevotes"].rank(ascending=False)
presidents_winners = presidents[presidents["rank"] == 1]
presidents_winners = pd.DataFrame(presidents_winners)
presidents_winners["prev_winner"] = presidents_winners.groupby("state")["party_simplified"].shift(-1)
presidents_winners = presidents_winners.dropna(subset=["prev_winner"])
presidents_winners["change_of_party"] = np.where(presidents_winners["party_simplified"] == presidents_winners["prev_winner"], "0", "1")
presidents_winners["change_of_party"] = pd.to_numeric(presidents_winners["change_of_party"])
presidents_grouped = presidents_winners.groupby("state")["change_of_party"].sum()
presidents_grouped = pd.DataFrame(presidents_grouped)
presidents_grouped = presidents_grouped.sort_values(["change_of_party"], ascending=False)
print("Pořadí států dle počtu změn vítězné strany mezi jednotlivými prezidentskými volbami:")
print(presidents_grouped.head(51))
print("\n")

presidents = pd.DataFrame(presidents)
presidents_1st_2nd = presidents[(presidents["rank"] == 1) | (presidents["rank"] == 2)]
presidents_1st_2nd = pd.DataFrame(presidents_1st_2nd)
presidents_1st_2nd["2nd_cand_votes"] = presidents_1st_2nd.groupby("state")["candidatevotes"].shift(-1)
presidents_1st_2nd = presidents_1st_2nd[presidents_1st_2nd["rank"] == 1]
presidents_1st_2nd = presidents_1st_2nd.dropna(subset=["2nd_cand_votes"])
presidents_1st_2nd = pd.DataFrame(presidents_1st_2nd)
presidents_1st_2nd["margin"] = presidents_1st_2nd["candidatevotes"] - presidents_1st_2nd["2nd_cand_votes"]
presidents_1st_2nd["relative_margin"] = (presidents_1st_2nd["margin"] / presidents_1st_2nd["candidatevotes"])
presidents_1st_2nd = presidents_1st_2nd.sort_values(["relative_margin", "margin"])
print("10 států s nejmenším absolutním rozdílem v počtu hlasů mezi vítězem a druhým kandidátem:")
print(presidents_1st_2nd.head(10))
