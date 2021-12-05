import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

pd.set_option('display.max_columns', None)

r = requests.get(
    "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/auto.csv"
)
open("auto.csv", "wb").write(r.content)

data = pd.read_csv("auto.csv", na_values=["?"])
print(data.sort_values("origin").tail())
data = data.dropna()
print(data.dtypes)

data_grouped = data.groupby(["year"])["mpg"].mean()
# data_grouped.plot(kind="bar")
data_pivot = pd.pivot_table(data, values="mpg", index="year", columns="origin", aggfunc=np.mean)
data_pivot.plot()
# plt.show()

X = data.drop(columns=["origin", "name"])
y = data["origin"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = DecisionTreeClassifier(random_state=42)

clf = GridSearchCV(model, param_grid={'max_depth': [1, 3, 5, 7], 'min_samples_leaf': [1, 3, 5, 7, 11]}, scoring="f1_weighted")
clf.fit(X_train, y_train)

print(clf.best_params_)
print(round(clf.best_score_, 2))

model_1 = DecisionTreeClassifier(random_state=42, max_depth=7, min_samples_leaf=3)
clf = model_1.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"))
