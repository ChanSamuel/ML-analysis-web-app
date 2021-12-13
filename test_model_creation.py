import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression

# Create the model.
print('Training the model.')
data = pd.read_csv('testfiles/Iris.csv')
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
clf = LogisticRegression(random_state=0, max_iter=1000).fit(X, y)

filename = 'test_model_iris.sav'
# Save the model to disk
print('Saving model to disk')
pickle.dump(clf, open('testfiles/' + filename, 'wb'))