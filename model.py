import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle

df = pd.read_csv("concrete_data.csv")

x = df.drop('Strength',axis=1)
y = df['Strength']

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)

rfr_model = RandomForestRegressor()
rfr_model.fit(X_train,y_train)

y_pred = rfr_model.predict(X_test)
print("Training Accuracy: ", rfr_model.score(X_train, y_train))

accuracy = metrics.r2_score(y_test, y_pred)
print("Accuracy: ", accuracy)

pickle.dump(rfr_model, open('rfr_concrete_data.pkl','wb'))