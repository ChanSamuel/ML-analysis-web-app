from multimethod import multimethod
from analysers import Analyser
from streamlit import cache
from handlers.simple import StandardHandler
from handlers.testing import TestHandler


class CorrAnalyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Calculate and return the correlation between features as a dataframe.
        Also returns any strong correlations (> 0.7) as a dictionary of key-value pairs where the key is
        a string of the form 'feature1 & feature2', and the value is the correlation strength.

        :return: a tuple (dataframe, dictionary)
        """

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        tbl = hdlr.get_tabular()
        corr_tbl = tbl.corr()

        # Find any strong correlations by checking each entry in the correlation table.
        strong_corrs = {}
        for i in range(corr_tbl.shape[0]):
            for j in range(corr_tbl.shape[0]):
                # Once we reach the diagonal we stop searching this row, because we want
                # to restrict our search to the 'lower triangle' to avoid duplicates.
                if i == j:
                    break

                r = abs(corr_tbl.iloc[i, j])  # Take the strength of the correlation.

                # If the correlation is stronger or equal to 0.7, consider it to be strong.
                if r >= 0.7:
                    key = str(tbl.columns[i]) + ' & ' + str(tbl.columns[j])
                    strong_corrs[key] = r

        # Return the correlation table as well as any strong correlations as a dictionary.
        return corr_tbl, strong_corrs

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """
        Calculate and display the correlations between features.
        Also reports any strong correlations (> 0.7).
        """

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        tbl = hdlr.get_tabular()
        corr_tbl = tbl.corr()
        print(corr_tbl)

        # Find any strong correlations by checking each entry in the correlation table.
        strong_corrs = {}
        for i in range(corr_tbl.shape[0]):
            for j in range(corr_tbl.shape[0]):
                # Once we reach the diagonal we stop searching this row, because we want
                # to restrict our search to the 'lower triangle'.
                if i == j:
                    break

                r = abs(corr_tbl.iloc[i, j])  # Take the strength of the correlation.

                # If the correlation is stronger or equal to 0.7, consider it to be strong.
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
