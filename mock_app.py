from handlers.simple import StandardHandler
from analysers import accuracy, corr, f1, mean_std, mse, r2, shape, show_data

filename = 'test_model_iris.sav'

# Obtain the saved files.
print('Loading file objects')
data_file = open('testfiles/Iris.csv')
model_file = open('testfiles/' + filename, 'rb')

# Creating Handler.
print('Creating Handler')
sh = StandardHandler(data_file, model_file, problem_type='classification', target_idx=-1)

# Invoking analysis operations.
print('Doing analysis')
shape.analyse(sh)
accuracy.analyse(sh)
show_data.analyse(sh)
mean_std.analyse(sh)
corr.analyse(sh)
f1.analyse(sh)
# mse.analyse(sh)
# r2.analyse(sh)
