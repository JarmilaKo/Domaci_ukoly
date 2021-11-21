import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    ConfusionMatrixDisplay,
    recall_score
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/water-potability.csv")
open("water-potability.csv", 'wb').write(r.content)

df = pd.read_csv("water-potability.csv")
df = df.dropna()
# print(df["Potability"].value_counts(normalize=True))

X = df.drop(columns="Potability")
y = df["Potability"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# print(X_train.shape, X_test.shape)
# print(y_train.shape, y_test.shape)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

clf = KNeighborsClassifier(n_neighbors=13)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test, display_labels=clf.classes_, cmap=plt.cm.Blues)
plt.show()

ks = [1, 3, 5, 7, 9, 11, 13, 15, 17]
f1_scores = []
precision_scores = []
accuracy_scores = []
recall_scores = []
for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))
    precision_scores.append(precision_score(y_test, y_pred))
    accuracy_scores.append(accuracy_score(y_test, y_pred))
    recall_scores.append(recall_score(y_test, y_pred))

plt.plot(ks, f1_scores)
plt.plot(ks, precision_scores)
plt.plot(ks, accuracy_scores)
plt.plot(ks, recall_scores)
plt.legend(["f1_scores", "precision_scores", "accuracy_scores", "recall_scores"])
# plt.show()

