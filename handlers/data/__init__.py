from handlers import Handler
from handlers.utilities import UnsupportedMethodException


class DataHandler(Handler):
    """
    The parent abstract class for all DataHandlers.
    This class is designed to be used as an interface, thus this class has no implementation.
    Each Handler which handles data should extend this class rather than Handler.
    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        super().__init__()

    def load_data(self, file):
        """
        Loads and returns the data from a given file.
        Must be implemented by the subclass.

        :returns: the data.
        """
        raise NotImplementedError('get_data must be overridden!')

    def get_tabular(self):
        """
        Obtain a tabular representation of the data.
        It is possible that some DataHandlers may not support this method.
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

    def unsupported_methods(self):
        """
        Returns the list of unsupported analysts/methods.
        The names in the returned list are the names based off of models.get_analyst_names()

        :return: the list of unsupported Analyst names.
        """
        raise NotImplementedError('unsupported_methods must be overridden!')

    def n_samples_op(self):
        """
        Perform an analysis to return the number of samples in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('n_samples_op must be overridden!')

    def n_features_op(self):
        """
        Perform an analysis to return the number of features in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('n_features_op must be overridden!')

    def accuracy_op(self):
        """
        Unsupported method, calling this will raise an UnsupportedMethodException.
        """
        raise UnsupportedMethodException('Accuracy analysis is not supported for DataHandler, use ModelHandler instead')
