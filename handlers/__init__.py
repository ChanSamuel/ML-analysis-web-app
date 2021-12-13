def all_problem_names():
    return 'classification', 'regression'


class Handler:
    """
    The parent class of all Handler types. It contains unimplemented template methods for loading the model/data.

    The goal of a Handler object is to load the data and model from their respective files and store them as fields.
    All other methods in Handler are there for convenience.

    Analysers in the 'analysers' package can then use these fields and methods to analyse
    the model and report the results.

    It is recommended that subclasses override all methods, with unsupported methods raising an
    exceptions.UnsupportedMethodException

    It is recommended that at least the following pre-conditions should be checked by the corresponding analyst method:
     - If the problem type (classification or regression) of this Handler is suitable for this analysis.
     - If any additional handlers passed as parameters are of the correct implementation.

    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        pass

    def get_tabular(self):
        """
        Obtain a tabular representation of the data.
        It is possible that some Handlers may not support this method.
        Must be implemented by subclass.

        :returns: the data as a Pandas dataframe.
        """
        raise NotImplementedError('get_tabular must be overridden!')

    def get_data(self):
        """
        Return the loaded data in some suitable format.
        The format is decided by the subclass.
        Must be implemented by subclass.

        :returns: the loaded data.
        """
        raise NotImplementedError('get_data must be overridden!')

    def load_data(self, file):
        """
        Loads and returns the data from a given file.
        Must be implemented by the subclass.

        :returns: the data.
        """
        raise NotImplementedError('get_data must be overridden!')

    def load_model(self, file):
        """Load and return the file as a model in some format."""
        raise NotImplementedError('load_model must be overridden!')

    def predict(self):
        """
        Return the predictions for each datapoint using the stored model in this ModelHandler.
        Should return a dataframe with a column for the actual target labels, and a column for the predicted
        target labels.
        """
        raise NotImplementedError('predict must be overridden!')

    def predict_proba(self):
        """
        Return the prediction probabilities using the stored model in this ModelHandler.
        May not necessarily be supported by the subclass' implementation.
        """
        raise NotImplementedError('predict_proba must be overridden!')
