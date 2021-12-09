import pickle

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score

from handlers import Handler, all_analyst_names, all_problem_names
from handlers.utilities import FileLoadingException, UnsupportedMethodException


class StandardHandler(Handler):
    """
    Is able to handle and load in tabular data (.csv format) with a pickled sklearn model.
    StandardHandler should support most analysis types.
    """

    def supported_methods(self):
        """
        Returns the list of supported analysts/methods.
        The names in the returned list are the names based off of handlers.all_analyst_names().
        The contents of the returned list determine what analysis' the app module sees this Handler is
        capable of.

        :return: the list of supported analyst names.
        """

        return all_analyst_names()

    # ================================= FILE LOADING METHODS =================================

    def load_data(self, file):
        """
        Loads and returns the data as a Pandas dataframe from a given .csv file.
        Raises an Exception if file loading fails.

        :raises: FileLoadingException
        :returns: the data as a Pandas dataframe.
        """

        # Pre-condition checks.
        if file is None:
            raise ValueError('Precondition check: File cannot be None')

        data = pd.read_csv(file)

        # Post-condition check
        if data is None:
            raise FileLoadingException('Something went wrong when loading in the file: read_csv produced None')

        return data

    def load_model(self, file):
        """
        Load and return the pickled file as an sklearn model.
        The file parameter can be obtained by using open(file_name, 'rb') or by any other means.

        :param: file : the pickled file containing the model.
        """

        return pickle.load(file)

    # ================================= CONSTRUCTOR METHOD =================================

    def __init__(self, data_file, model_file, problem_type, target_idx):
        """
        Constructs this object by loading in the data and model from the given files and storing them as fields.
        Raises an exception if file loading fails.
        The file parameter can be obtained by using open(file_name, 'rb') or by any other means.

        :param: file : the file to handle.
        :param: problem_type : MUST be an item returned by handlers.utilities.get_problem_names() ('classification' or
        'regression')
        :param: target_idx : the index of the target feature in the dataset (should usually be -1 for last).
        :raises: FileLoadingException
        """

        super().__init__()

        # Pre-condition checks.
        if not isinstance(problem_type, str):
            raise ValueError(f'Precondition: problem_type should be a string got {type(problem_type)}')
        if not (problem_type in all_problem_names()):
            raise ValueError('Precondition: problem_type should match an item returned by '
                             'handlers.utilities.get_problem_names(), instead found ' + problem_type)
        if not isinstance(target_idx, int):
            raise ValueError('Precondition: target_idx must be an int')

        self.problem_type = problem_type  # A string which is either classification or regression.
        self.target_idx = target_idx  # The column index of the target class from the data.
        self.data = self.load_data(data_file)  # The raw data as loaded by load_data().
        self.X = self.data.drop(self.data.columns[self.target_idx], axis=1)  # The training features.
        self.y = self.data.iloc[::, self.target_idx]  # The target column.
        self.model = self.load_model(model_file) # The sklearn trained model.

    # ================================= PREDICTION METHODS =================================

    def predict(self):
        """
        Returns a dataframe with a column for the actual target labels, and a column for the predicted
        target labels, for each datapoint in self.get_data().

        The returned dataframe's two columns are [actual, predicted]. Retrieving the 'actual' column
        can be done with either df['actual'] or df.iloc[:, 0].

        :return: a dataframe of shape (n_samples, 2)
        """

        actuals = self.y
        preds = self.model.predict(self.X)

        # Post-condition checks
        if len(actuals) != len(preds):
            raise ValueError('Post-condition: length of actuals does not match length of preds')

        return pd.DataFrame({'actual': actuals, 'predicted': preds})

    def predict_proba(self):
        """
        Return the prediction probabilities of the stored model as a dataframe.
        The class name of each column in the returned dataframe is given in df.columns.

        :return: a dataframe of shape (n_samples, n_classes)
        """

        # Pre-condition checks
        if self.model is None:
            raise ValueError('Precondition: self.model cannot be None')
        if not hasattr(self.model, 'predict_proba'):
            raise UnsupportedMethodException('predict_proba is not supported for self.model')

        preds = self.model.predict_proba(self.X)

        df = pd.DataFrame(preds)
        df.columns = self.model.classes_  # Set the predicted class names.

        return df

    # ================================= DATA GETTER METHODS =================================

    def get_tabular(self):
        """
        Obtain a tabular representation of the data.

        :return: the data as a Pandas dataframe.
        """

        return self.get_data()

    def get_data(self):
        """
        Return the loaded data as a Pandas dataframe.
        Note that the returned dataframe is not a copy, and is thus open for mutation;
        for performance reasons, defensive cloning cannot be utilised to prevent mutation.

        :return: the loaded data as a dataframe.
        """

        if self.data is None:
            raise ValueError('Precondition: self.data should not be None')
        if len(self.data) <= 0:
            raise ValueError(f'Precondition: self.data must have positive length, '
                             f'instead found length {len(self.data)}')
        return self.data

    # ================================= ANALYSIS METHODS =================================

    def shape_op(self):
        """
        Perform an analysis to get the number of samples and features in the data.
        If the problem_type is classification, then this method will also analyse number of classes.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """

        # Pre-condition checks.
        if self.data is None:
            raise ValueError('Precondition: self.data is None')
        if not (self.problem_type in all_problem_names()):  # Check that the current problem type is valid.
            raise ValueError(f'Precondition: problem_type of {self.problem_type} is not supported')

        # Now, we do the analysis.
        nrows = self.data.shape[0]
        ncols = self.data.shape[1]

        # Display the results.
        if self.problem_type == all_problem_names()[0]:  # If doing a classification problem.
            nclasses = len(self.y.unique())
            print(f'Data has {nrows} samples, {ncols} features (including target feature), and {nclasses} classes.')
        else:
            print(f'Data has {nrows} samples, {ncols} features (including target feature).')

        samples_per_feature = round(nrows / ncols, 2)
        if samples_per_feature < 5:
            print(f'There are {samples_per_feature} samples per feature. Consider increasing the number of samples '
                  f'or decreasing the number features.')
        else:
            print(f'There are {samples_per_feature} samples per feature.')

    def accuracy_op(self):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.

        :return: None
        """

        if self.problem_type == all_problem_names()[1]:  # Check that the current problem type is not regression.
            raise ValueError(f'Precondition: problem_type of {self.problem_type} is not supported')

        df = self.predict()
        acc = accuracy_score(df['actual'], df['predicted'])

        # Display the results.
        print(f'Accuracy is {round(acc * 100, 3)}% (3 dp)')

    def show_data_op(self):
        """Show a few entries of the data."""
        print(self.get_data())

    def mean_std_op(self):
        """Calculate and show the mean and standard deviation for every feature of the data."""
        tbl = self.get_tabular()

        # Calculate and transpose the returned results so that the columns correspond to the feature names.
        means = pd.DataFrame(np.mean(tbl, axis=0)).T
        stds = pd.DataFrame(np.std(tbl, axis=0)).T

        # Join the two tables.
        displayed_table = pd.concat([means, stds])
        displayed_table.index = ['Mean', 'Std']

        # Display the results.
        print(displayed_table)

    def corr_op(self):
        """
        Calculate and display the correlations between features.
        Also reports any strong correlations (> 0.7).
        """
        tbl = self.get_tabular()
        corr_tbl = tbl.corr()
        print(corr_tbl)

        # Find any strong correlations.
        strong_corrs = {}
        for i in range(corr_tbl.shape[0]):
            for j in range(corr_tbl.shape[0]):
                if i != j: # Skip comparisons between same features.
                    r = abs(corr_tbl.iloc[i, j])
                    if r >= 0.7:
                        key = str(tbl.columns[i]) + ' & ' + str(tbl.columns[j])
                        strong_corrs[key] = r

        # Report any strong correlations.
        if len(strong_corrs) >= 0:
            print(f'{len(strong_corrs)} strong correlations found:')
            for kv in strong_corrs.items():
                key = kv[0]
                value = kv[1]
                print(f'{key}: {round(value, 3)}')
        else:
            print('No strong correlations found.')

    def f1_score_op(self):
        """
        Calculate the f1 score(s) for the current model.
        If current model is multi-class, then the F1-score for each class will be shown.
        Raises UnsupportedMethodException if current model is not a classification model.

        :raises: UnsupportedMethodException
        """

        # Preconditions.
        if self.problem_type != 'classification':
            raise UnsupportedMethodException('F1 score cannot be used on non-classification model.')

        # Give the f1 scores for each class if not binary classification.
        if len(self.model.classes_) == 2:
            score = f1_score(self.y, self.model.predict(self.X))
            print('The F1 score is:', score)
        else:
            scores = f1_score(self.y, self.model.predict(self.X), average=None)
            score_table = pd.DataFrame(columns=self.model.classes_)
            score_table.loc[0] = scores
            print('The F1 scores for each class are:')
            print(score_table)

    def mse_score_op(self):
        """
        Calculate the MSE (Mean Squared Error) for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        """

        # Preconditions.
        if self.problem_type != 'regression':
            raise UnsupportedMethodException('MSE cannot be used on non-regression model.')

        score = mean_squared_error(self.y, self.model.predict(self.X))
        print('The MSE is:', score)

    def r2_score_op(self):
        """
        Calculate the R^2 (Coefficient of Determination) score for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        """

        # Preconditions.
        if self.problem_type != 'regression':
            raise UnsupportedMethodException('R^2 cannot be used on non-regression model.')

        score = r2_score(self.y, self.model.predict(self.X))
        print('The R^2 score is:', score)
