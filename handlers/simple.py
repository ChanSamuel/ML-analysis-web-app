import pandas as pd

from handlers import Handler, all_analyst_names, all_problem_names
from handlers.utilities import FileLoadingException


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
        try:
            data = pd.read_csv(file)
            if data is None:
                raise FileLoadingException('Something went wrong when loading in the file: read_csv produced None')

            return data
        except FileNotFoundError:
            raise FileLoadingException('File was not found!')
        except: # Re-raise the exception.
            raise FileLoadingException('Something went wrong when loading in the file.')

    def load_model(self, file):
        """Load and return the file as a model in some format."""
        raise NotImplementedError('load_model must be overridden!')

    # ================================= CONSTRUCTOR METHOD =================================

    def __init__(self, file, problem_type):
        """
        Constructs this object by loading in the data and model from the given files and storing them as fields.
        Raises an exception if file loading fails.

        :param: file : the file to handle.
        :param: problem_type : MUST be an item returned by handlers.utilities.get_problem_names() ('classification' or
        'regression')
        :raises: FileLoadingException
        """

        super().__init__()

        # Pre-condition checks.
        if ~isinstance(problem_type, str):
            raise ValueError('problem_type should be a string')
        if ~(problem_type in all_problem_names()):
            raise ValueError('problem_type should match an item returned by handlers.utilities.get_problem_names()')

        self.problem_type = problem_type
        self.data = self.load_data(file)

    # ================================= PREDICTION METHODS =================================

    def predict(self, test_data):
        """
        Return the predictions for each datapoint using the stored model in this ModelHandler.
        Should return a dataframe with a column for the actual target labels, and a column for the predicted
        target labels.
        """
        raise NotImplementedError('predict must be overridden!')

    def predict_proba(self, test_data):
        """
        Return the prediction probabilities using the stored model in this ModelHandler.
        May not necessarily be supported by the subclass implementation.
        """
        raise NotImplementedError('predict_proba must be overridden!')

    # ================================= DATA GETTER METHODS =================================

    def get_tabular(self):
        """
        Obtain a tabular representation of the data.

        :returns: the data as a Pandas dataframe.
        """

        return self.get_data()

    def get_data(self):
        """
        Return the loaded data as a Pandas dataframe.
        Note that the returned dataframe is not a copy, and is thus open for mutation;
        for performance reasons, defensive cloning cannot be utilised to prevent mutation.

        :returns: the loaded data as a dataframe.
        """

        return self.data

    # ================================= ANALYSIS METHODS =================================

    def shape_op(self):
        """
        Perform an analysis to get the number of samples and features in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """

        # Pre-condition checks.
        if self.data is None:
            raise ValueError('Pre-condition failed: self.data is None')
        if ~(self.problem_type in all_problem_names()):
            raise ValueError(f'Pre-condition failed: problem_type of {self.problem_type} is not supported')

        # Now, we do the analysis.
        nrows = self.data.shape[0]
        ncols = self.data.shape[1]

        # Display the results.
        print(f'Data has {nrows} rows and {ncols} features.')

    def accuracy_op(self, test_data):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('accuracy_op must be overridden!')
