import yfinance as yf
import pandas as pd
pd.set_option('display.max_columns', None)

csco = yf.Ticker("CSCO")
csco_df = csco.history(period="5y")
# print(csco_df.head())
csco_df["Close"].plot()
# print(csco_df["Close"].autocorr(lag=1))

from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
# plot_acf(csco_df["Close"])
# plt.show()

# from statsmodels.tsa.seasonal import seasonal_decompose
# decompose = seasonal_decompose(csco_df["Close"], model='multiplicative', period=365)
# decompose.plot()
# plt.show()

from statsmodels.tsa.ar_model import AutoReg
mod = AutoReg(csco_df["Close"], lags=100, trend="t", seasonal=False)
res = mod.fit()
predictions = res.predict(start=csco_df.shape[0], end=csco_df.shape[0]+5)
predictions = pd.DataFrame(predictions, columns=["Prediction"])
df_with_predictions = pd.concat([csco_df, predictions])
df_with_predictions[["Close", "Prediction"]].tail(100).plot()
plt.show()
