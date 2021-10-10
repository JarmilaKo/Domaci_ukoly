import pandas as pd
import requests

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

lexikon = pd.read_csv("lexikon-zvirat.csv", sep=";")
lexikon = lexikon.dropna(how="all", axis="columns")
lexikon = lexikon.dropna(how="all", axis="rows")
lexikon = lexikon.set_index("id")


def check_url(radek):
    if isinstance(radek.image_src, str):
        if radek.image_src.startswith("https://zoopraha.cz/images/"):
            if radek.image_src.lower().endswith(".jpg"):
                return 1
    return 0


lexikon["kontrola"] = lexikon.apply(check_url, axis=1)
print(lexikon.groupby("kontrola")["kontrola"].count())
