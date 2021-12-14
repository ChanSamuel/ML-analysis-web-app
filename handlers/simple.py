import pickle

import pandas as pd

from handlers import Handler, all_problem_names
from handlers.exceptions import FileLoadingException, UnsupportedMethodException

from warnings import warn


def warning(msg):
    """
    Raises a warning to inform the user but not interrupt execution.
    :param msg: The warning message.
    """
    warn(msg)


def validate_data(data):
    """
    Validates the given dataframe by throwing an exception or warning if the data
    does not meet the following criteria:
    1). Dataframe contains atleast one missing value (warning).
    2). Dataframe contains no rows (exception).
    3). Dataframe contains only 1 column (exception).

    A warning raised may also be accompanied by a correction to the data, such
    as in the case of missing values (rows will be dropped).

    :param data: The dataframe loaded in.
    """

    if data is None:
        raise ValueError('Preconditions: Data cannot be None')
    if len(data) == 0:
        raise ValueError('Data cannot be empty!')
    if data.shape[1] <= 1:
        raise ValueError('Data must be greater than 1 column.')

    n_missing = data.isnull().sum().sum()
    if n_missing > 0:
        # Drop the rows with missing values.
        data.dropna(axis=0, how='any', inplace=True)

        # Re-check that the data is still of acceptable length.
        if len(data) == 0:
            raise ValueError('Data cannot be empty!')

        # Provide a warning with a message informing the user what just happened.
        warning(f'{n_missing} missing values were found and dropped.')


class StandardHandler(Handler):
    """
    Is able to handle and load in tabular data (.csv format) with a pickled sklearn model.
    StandardHandler is the default handler, it should be supported by most if not all analyser types.
    See handlers.Handler for a description of what a Handler does.
    """

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
        validate_data(data)

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
        self.model = self.load_model(model_file)  # The sklearn trained model.

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
        for performance reasons, defensive cloning should not be used to prevent mutation.

        :return: the loaded data as a dataframe.
        """

        if self.data is None:
            raise ValueError('Precondition: self.data should not be None')
        if len(self.data) <= 0:
            raise ValueError(f'Precondition: self.data must have positive length, '
                             f'instead found length {len(self.data)}')
        return self.data
