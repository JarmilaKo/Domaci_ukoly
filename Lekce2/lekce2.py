import requests
import pandas as pd
import numpy as np
import datetime

pd.set_option('display.max_columns', None)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/data_with_ids.csv")
open("data_with_ids.csv", 'wb').write(r.content)

data_with_ids = pd.read_csv("data_with_ids.csv")
# print(data_with_ids.head())

# print(data_with_ids.shape[0])
# print(data_with_ids["bank_id"].nunique())

data_with_ids_unique = data_with_ids.drop_duplicates(ignore_index=True)
# print(data_with_ids_unique.shape[0])
# print(data_with_ids.nunique())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/covid_data.csv")
open("covid_data.csv", 'wb').write(r.content)

covid_data = pd.read_csv("covid_data.csv")
covid_data = covid_data.drop_duplicates(subset="date", keep="last")

# print(covid_data.head())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices.csv")
open("invoices.csv", 'wb').write(r.content)

invoices = pd.read_csv("invoices.csv")
invoices["date_converted"] = pd.to_datetime(invoices["invoice_date"], format="%d. %m. %Y")
invoices["due_date"] = pd.Timedelta("P60D") + invoices["date_converted"]
today_date = datetime.datetime(2021, 9, 1)
today_date2 = datetime.datetime.now()
invoices["status"] = np.where(invoices["due_date"]< today_date, "po_splatnosti", "pred_splatnosti")
# print(invoices.groupby("status")["amount"].sum())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices_2.csv")
open("invoices_2.csv", 'wb').write(r.content)

invoices_2 = pd.read_csv("invoices_2.csv")
invoices_2["invoice_date"] = pd.to_datetime(invoices_2["invoice_date"], format="%d. %m. %Y")
invoices_2["payment_date"] = pd.to_datetime(invoices_2["payment_date"], format="%d. %m. %Y")
invoices_2_paid = invoices_2.dropna().reset_index(drop=True)
invoices_2_paid["paid_in"] = invoices_2_paid["payment_date"] - invoices_2_paid["invoice_date"]

average_payment_data = pd.DataFrame(invoices_2_paid.groupby(["customer"])["paid_in"].mean())
average_payment_data = pd.DataFrame(average_payment_data)
# print(average_payment_data.head())

invoices_2_not_paid = invoices_2[invoices_2["payment_date"].isna()]
invoices_2_not_paid = pd.merge(invoices_2_not_paid, average_payment_data, on=["customer"], how="outer")
invoices_2_not_paid["expected_payment_date"] = invoices_2_not_paid["invoice_date"] + pd.to_timedelta(invoices_2_not_paid["paid_in"], unit="D")
invoices_2_not_paid["expected_payment_date"] = invoices_2_not_paid["expected_payment_date"].dt.date

# print(invoices_2_not_paid.head())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/signal_monitoring.csv")
open("signal_monitoring.csv", 'wb').write(r.content)

signal_monitoring = pd.read_csv("signal_monitoring.csv")
signal_monitoring["event_date_time"] = pd.to_datetime(signal_monitoring["event_date_time"])
signal_monitoring.head()

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/ioef.csv")
open("ioef.csv", 'wb').write(r.content)

ioef = pd.read_csv("ioef.csv")
ioef["rank"] = ioef.groupby(["Index Year"])["Overall Score"].rank(ascending=False)
ioef_sorted = ioef.sort_values(["Name", "Index Year"])
ioef_sorted["Rank Previous Year"] = ioef_sorted.groupby(["Name"])["rank"].shift()
# print(ioef_sorted.head())

ioef_sorted["Rank Change"] = ioef_sorted["rank"] - ioef_sorted["Rank Previous Year"]
ioef_sorted_czech = ioef_sorted[ioef_sorted["Name"] == "Czech Republic"]
# print(ioef_sorted_czech.tail())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/baroko_half_marathon.csv")
open("baroko_half_marathon.csv", 'wb').write(r.content)

baroko_half_marathon = pd.read_csv("baroko_half_marathon.csv")
baroko_half_marathon = baroko_half_marathon.sort_values(["Jméno závodníka", "Ročník", "Rok závodu"])
baroko_half_marathon["FINISH"] = pd.to_datetime(baroko_half_marathon["FINISH"], format="%H:%M:%S")
baroko_half_marathon["FINISH_previous"] = baroko_half_marathon.groupby(["Jméno závodníka", "Ročník"])["FINISH"].shift()
baroko_half_marathon = baroko_half_marathon.dropna(subset=["FINISH_previous"]).reset_index()
# baroko_half_marathon = baroko_half_marathon(baroko_half_marathon["FINISH", "FINISH_previous"])
baroko_half_marathon["Rozdil_casu"] = baroko_half_marathon["FINISH"] - baroko_half_marathon["FINISH_previous"]

# baroko_half_marathon["zmena"] = np.where(baroko_half_marathon["Rozdil_casu"] > 0, "zlepseni", "zhorseni")

print(baroko_half_marathon.head())
