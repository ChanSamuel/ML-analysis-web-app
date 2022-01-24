import pickle
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

# Create the model.
print('Training the model.')
data = pd.read_csv('testfiles/Boston.csv')

# Shuffle the dataset.
data = data.sample(frac=1).reset_index(drop=True)
split_idx = (len(data) // 4)  # The quarter way point.

# Train on 3/4 of the data.
X_train = data.iloc[split_idx:, :-1]
y_train = data.iloc[split_idx:, -1]
clf = DecisionTreeRegressor(random_state=0).fit(X_train, y_train)

# Save 1/4 of data into a .csv file for testing.
test_data = data.iloc[0:split_idx, :]
test_data.to_csv('testfiles/Boston_test.csv', index=False)

# Save the model to disk
filename = 'test_model_boston.sav'
print('Saving model to disk')
pickle.dump(clf, open('testfiles/' + filename, 'wb'))
