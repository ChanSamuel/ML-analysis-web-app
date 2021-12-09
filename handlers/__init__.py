def all_analyst_names():
    """
    Returns the formal names of all analyst methods.
    Used by Handler.supported_methods() to indicate which analysis methods are supported.
    Everytime a new analyst method is implemented, the returned list should be updated.
    """
    names = ['shape', 'accuracy', 'show_data', 'mean_std', 'corr', 'f1_score', 'mse_score', 'r2_score']
    return names


def all_problem_names():
    return 'classification', 'regression'


class Handler:
    """
    The parent class of all Handler types. It contains unimplemented template methods for loading the model/data,
    among other things.

    Subclasses of Handler have methods which perform a specific analysis of the data or model
    (i.e., get the number of samples, check for class imbalance, look at the accuracy of the model, etc)
    and display the analysis findings.

    Handler.supported_methods() returns a list whose contents are the names of the supported analysis types
    corresponding to the implemented analysis methods of the subclasses. Each subclass MUST override
    Handler.supported_methods() in order to indicate to the app module which methods can be called.
    To accomplish this, handlers.all_analyst_names() should be used, as it provides a consistent
    naming scheme to refer to each analysis method.

    All of Handler's methods should also preferably be overridden, with unsupported methods raising a
    utilities.UnsupportedMethodException.

    At least the following pre-conditions should be checked by the corresponding analyst method:
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
        May not necessarily be supported by the subclass implementation.
        """
        raise NotImplementedError('predict_proba must be overridden!')

    def supported_methods(self):
        """
        Returns the list of supported analysts/methods.
        The elements of the returned list are in accordance with handlers.all_analyst_names().
        The contents of the returned list determine what analysis' the app module sees this Handler is
        capable of.

        :return: the list of supported Analyst names.
        """
        raise NotImplementedError('supported_methods must be overridden!')
