from handlers.simple import StandardHandler
from analysers import accuracy, corr, f1, mean_std, mse, r2, shape, show_data, xai_shap
from handlers.testing import TestHandler

filename = 'test_model_iris.sav'

# Obtain the saved files.
print('Loading file objects')
data_file = open('testfiles/Iris.csv')
model_file = open('testfiles/' + filename, 'rb')

# Creating Handler.
print('Creating Handler')
sh = TestHandler(data_file, model_file, problem_type='classification', target_idx=-1)

# Invoking analysis operations.
print('Doing analysis')

# First check that all operations are supported (they should be when using TestHandler).
fully_supported = shape.supports(sh) and accuracy.supports(sh) and show_data.supports(sh) and mean_std.supports(sh) \
    and corr.supports(sh) and f1.supports(sh) and xai_shap.supports(sh) and mse.supports(sh) and r2.supports(sh)

if fully_supported:
    shape.analyse(sh)
    accuracy.analyse(sh)
    show_data.analyse(sh)
    mean_std.analyse(sh)
    corr.analyse(sh)
    f1.analyse(sh)
    print('Doing SHAP')
    xai_shap.analyse(sh)
    # mse.analyse(sh)
    # r2.analyse(sh)
else:
    raise RuntimeError('Not fully supported.')
