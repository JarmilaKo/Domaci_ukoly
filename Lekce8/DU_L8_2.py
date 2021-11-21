import requests
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

df = pd.read_csv("MLTollsStackOverflow.csv")
# df = df.set_index("month")
# print(df.dtypes)
python = df["python"]
# python.plot()

from statsmodels.tsa.seasonal import seasonal_decompose
decompose = seasonal_decompose(python, model="multiplicative", period=12)
# decompose.plot()
# plt.show()

from statsmodels.tsa.holtwinters import ExponentialSmoothing
mod = ExponentialSmoothing(python, seasonal_periods=12, trend="additive", seasonal="multiplicative",
                           initialization_method="estimated",)
res = mod.fit()
predictions = res.predict(start=len(python), end=len(python) + 12)
predictions = pd.DataFrame(predictions, columns=["Prediction"])
python = pd.DataFrame(python)
python_with_predictions = pd.concat([python, predictions])
python_with_predictions.plot()
plt.show()
