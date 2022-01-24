from multimethod import multimethod
from analysers import Analyser
from handlers.simple import StandardHandler
from handlers.testing import TestHandler
from streamlit import cache


class ShowDataAnalyser(Analyser):
    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """Return the data."""
        return hdlr.get_data()

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """Show a few entries of the data."""
        print(hdlr.get_data())

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
