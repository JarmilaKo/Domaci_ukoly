import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "jarmila.kowolowska"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "L48J5Xbzm!Sg8Fgb"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

# inspector = inspect(engine)
# print(inspector.get_columns("dreviny"))

# 1. Pomocí SQL dotazu do databáze si připrav dvě pandas tabulky:
# tabulka smrk bude obsahovat řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska"
# tabulka nahodila_tezba bude obsahovat řádky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva"
smrk = pd.read_sql("SELECT * FROM \"dreviny\" WHERE dd_txt = 'Smrk, jedle, douglaska'", con=engine)
nahodila_tezba = pd.read_sql("SELECT * FROM \"dreviny\" WHERE druhtez_txt = 'Nahodilá těžba dřeva'", con=engine)

# 2.Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk. Pozor, řádky nemusí být seřazené podle roku.
smrk = smrk.sort_values(by="rok")
# smrk.plot(kind="bar", y="hodnota", x="rok", title="Těžba smrkového dřeva")
# plt.show()

# Vytvoř graf, který ukáže vývoj objemu těžby pro různé typy nahodilé těžby:
# Agreguj tabulku nahodila_tezba podle sloupce prictez_txt a na výsledek operace groupby zavolej metodu plot
# s parametrem legend=True.

nahodila_tezba.pivot_table(values="hodnota", index="rok", columns="prictez_txt", aggfunc=np.sum).plot()
plt.show()
