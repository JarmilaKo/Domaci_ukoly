import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("soybean-2-rot.csv")
print(data.head())

X = data.drop(columns=["class"])
y = data["class"]
print(X.shape)
input_features = list(X.columns)

encoder = OneHotEncoder()
X = encoder.fit_transform(X)
print(X.shape)

l_encoder = LabelEncoder()
y = l_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

f1_kompletni_model = f1_score(y_test, y_pred, average="weighted")
print("f1_score pro model se všemi proměnnými:", f1_kompletni_model)
# print(encoder.get_feature_names_out(input_features=input_features))

col_names = list(encoder.get_feature_names_out(input_features=input_features))
importance = list(clf.feature_importances_)
importance_join = pd.DataFrame({"col_names": col_names, "importance": importance}).sort_values("importance", ascending=False)
# print(importance_join)

X1 = data.drop(columns=["class", "plant-stand"])
X1 = encoder.fit_transform(X1)

X1_train, X1_test, y_train, y_test = train_test_split(X1, y, test_size=0.2, random_state=42, stratify=y)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X1_train, y_train)

y_pred = clf.predict(X1_test)

f1_score_bez_nejdulezitejsi = f1_score(y_test, y_pred, average="weighted")
print("f1 score pro model bez proměnné plant-stand:", f1_score_bez_nejdulezitejsi)
print("Rozdíl f1_score je: ", f1_kompletni_model - f1_score_bez_nejdulezitejsi)
# f1_score vyšlo téměř identicky.