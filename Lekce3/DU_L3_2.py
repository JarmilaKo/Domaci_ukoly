import requests
import pandas as pd

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

lexikon = pd.read_csv("lexikon-zvirat.csv", sep=";")
lexikon = lexikon.dropna(how="all", axis="columns")
lexikon = lexikon.dropna(how="all", axis="rows")
lexikon = lexikon.set_index("id")


def popisek(radek):
    popis = str(radek.title) + " preferuje následující typ stravy: "+ str(radek.food).lower() +\
            ". Konkrétně ocení když mu do misky přistanou " + str(radek.food_note).lower() + "." + "\n" +\
            "Jak toto zvíře poznáme: " + str(radek.description)
    return popis


lexikon["popisek"] = lexikon.apply(popisek, axis=1)

print(lexikon["popisek"][320])
