import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt

# Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").
# Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).
# Ve kterém měsíci dochází nejčastěji ke krádeži auta?

pd.set_option('display.max_columns', None)

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "jarmila.kowolowska"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "L48J5Xbzm!Sg8Fgb"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

# inspector = inspect(engine)
# print(inspector.get_columns("crime"))

motorvehicle_theft = pd.read_sql("SELECT * FROM \"crime\" WHERE \"PRIMARY_DESCRIPTION\" = 'MOTOR VEHICLE THEFT'", con=engine)
print(motorvehicle_theft.head())
motorvehicle_theft_auto = motorvehicle_theft[motorvehicle_theft["SECONDARY_DESCRIPTION"] == "AUTOMOBILE"].reset_index()
motorvehicle_theft_auto["DATE_OF_OCCURRENCE"] = pd.to_datetime(motorvehicle_theft_auto["DATE_OF_OCCURRENCE"])
motorvehicle_theft_auto["month"] = motorvehicle_theft_auto["DATE_OF_OCCURRENCE"].dt.month
motorvehicle_theft_auto_grouped = motorvehicle_theft_auto.groupby("month")["SECONDARY_DESCRIPTION"].count().plot()
plt.show()

# ke krádežím dochází nejčastějí v 9.měsíci
