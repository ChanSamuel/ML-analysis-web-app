import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression

from handlers.simple import StandardHandler

# Create the model.
# print('Training the model.')
# data = pd.read_csv('testfiles/Iris.csv')
# X = data.iloc[:, :-1]
# y = data.iloc[:, -1]
# clf = LogisticRegression(random_state=0, max_iter=1000).fit(X, y)

filename = 'test_model_iris.sav'
# Save the model to disk
# print('Saving model to disk')
# pickle.dump(clf, open('testfiles/' + filename, 'wb'))

# Obtain the saved files.
print('Loading file objects')
data_file = open('testfiles/Iris.csv')
model_file = open('testfiles/' + filename, 'rb')

# Creating Handler.
print('Creating Handler')
sh = StandardHandler(data_file, model_file, problem_type='classification', target_idx=-1)

# Invoking analysis operations.
print('Doing analysis')
sh.shape_op()
sh.accuracy_op()
sh.show_data_op()
sh.mean_std_op()
sh.corr_op()
