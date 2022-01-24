import pickle

import pandas as pd
from sklearn.tree import DecisionTreeRegressor

# Create the model.
print('Training the model.')
data = pd.read_csv('testfiles/Boston.csv')
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
clf = DecisionTreeRegressor(random_state=0).fit(X, y)

filename = 'test_model_boston.sav'
# Save the model to disk
print('Saving model to disk')
pickle.dump(clf, open('testfiles/' + filename, 'wb'))