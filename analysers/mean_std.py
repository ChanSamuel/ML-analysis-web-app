import numpy as np
import pandas as pd
from multimethod import multimethod
from analysers import Analyser
from handlers.simple import StandardHandler
from handlers.testing import TestHandler
from streamlit import cache


class MeanStdAnalyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Calculate and return the mean and standard deviation for every feature of the data.
        Returns a table of n columns and 2 rows. Columns represent the features, and rows are the
        mean and standard deviation respectively.

        :returns: dataframe of shape [2, n]
        """

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        tbl = hdlr.get_tabular()

        # Calculate and transpose the returned results so that the columns correspond to the feature names.
        means = pd.DataFrame(np.mean(tbl, axis=0)).T
        stds = pd.DataFrame(np.std(tbl, axis=0)).T

        # Join the two rows into one table.
        displayed_table = pd.concat([means, stds])
        displayed_table.index = ['Mean', 'Std']

        return displayed_table

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """Calculate and show the mean and standard deviation for every feature of the data."""

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        tbl = hdlr.get_tabular()

        # Calculate and transpose the returned results so that the columns correspond to the feature names.
        means = pd.DataFrame(np.mean(tbl, axis=0)).T
        stds = pd.DataFrame(np.std(tbl, axis=0)).T

        # Join the two rows into one table.
        displayed_table = pd.concat([means, stds])
        displayed_table.index = ['Mean', 'Std']

        # Display the results.
        print(displayed_table)

    def is_metric(self):
        """
        Returns whether the result of the analysis is a performance metric or not.
        :return: True if this analyser is a metric, false otherwise.
        """
        return False

    def model_type(self):
        """
        Returns the type of model this analyser supports.
        :return: can return any of the strings: 'classification', 'regression', or 'agnostic'.
        """
        return "agnostic"
