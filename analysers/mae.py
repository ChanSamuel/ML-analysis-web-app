from multimethod import multimethod
from sklearn.metrics import mean_absolute_error
from analysers import Analyser
from exceptions import UnsupportedMethodException
from handlers.simple import StandardHandler
from handlers.testing import TestHandler
from streamlit import cache


class MAEAnalyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Calculate and return the MAE (Mean Absolute Error) for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        :returns: The MAE score.
        """

        # Preconditions.
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'regression':
            raise UnsupportedMethodException('MAE cannot be used on non-regression model.')

        score = mean_absolute_error(hdlr.y, hdlr.model.predict(hdlr.X))
        return score

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """
        Calculate and return the MAE (Mean Absolute Error) for the current model.
        Raises UnsupportedMethodException if current model is not a regression model.

        :raises: UnsupportedMethodException
        """

        # Preconditions.
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'regression':
            raise UnsupportedMethodException('MAE cannot be used on non-regression model.')

        score = mean_absolute_error(hdlr.y, hdlr.model.predict(hdlr.X))

        print('The MAE score is:', score)

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
