from handlers.data import DataHandler


class TabularDataHandler(DataHandler):
    """
    Is able to handle and load in tabular data (.csv format).
    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        super().__init__()

    def load_data(self, file):
        """
        Loads and returns the data as a Pandas dataframe from a given .csv file.

        :returns: the data as a Pandas dataframe.
        """
        raise NotImplementedError('not yet developed')

    def get_tabular(self):
        """
        Obtain a tabular representation of the data.

        :returns: the data as a Pandas dataframe.
        """
        raise NotImplementedError('not yet developed')

    def get_data(self):
        """
        Return the loaded data as a Pandas dataframe.

        :returns: the loaded data.
        """
        raise NotImplementedError('not yet developed')

    def unsupported_methods(self):
        """
        Returns the list of unsupported analysts/methods.
        The names in the returned list are the names based off of models.get_analyst_names()

        :return: the list of unsupported Analyst names.
        """
        raise NotImplementedError('not yet developed')

    def n_samples_op(self):
        """
        Perform an analysis to return the number of samples in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('not yet developed')

    def n_features_op(self):
        """
        Perform an analysis to return the number of features in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('not yet developed')

