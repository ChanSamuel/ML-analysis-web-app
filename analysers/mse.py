from multimethod import multimethod
from sklearn.metrics import mean_squared_error
from analysers import Analyser
from exceptions import UnsupportedMethodException
from handlers.simple import StandardHandler
from handlers.testing import TestHandler
from streamlit import cache


class MSEAnalyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Calculate and return the MSE (Mean Squared Error) for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        :returns: a number representing the MSE.
        """

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        # Preconditions.
        if hdlr.problem_type != 'regression':
            raise UnsupportedMethodException('MSE cannot be used on non-regression model.')

        score = mean_squared_error(hdlr.y, hdlr.model.predict(hdlr.X))
        return score

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """
        Calculate the MSE (Mean Squared Error) for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        """

        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')

        # Preconditions.
        if hdlr.problem_type != 'regression':
            raise UnsupportedMethodException('MSE cannot be used on non-regression model.')

        score = mean_squared_error(hdlr.y, hdlr.model.predict(hdlr.X))
        print('The MSE is:', score)

    def is_metric(self):
        """
        Returns whether the result of the analysis is a performance metric or not.
        :return: True if this analyser is a metric, false otherwise.
        """
        return True

    def model_type(self):
        """
        Returns the type of model this analyser supports.
        :return: can return any of the strings: 'classification', 'regression', or 'agnostic'.
        """
        return "regression"
