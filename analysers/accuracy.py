from multimethod import multimethod
from sklearn.metrics import accuracy_score
from analysers import Analyser
from streamlit import cache
from handlers.simple import StandardHandler
from handlers.testing import TestHandler


class AccuracyAnalyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.

        :return: an accuracy score between 0 and 1.
        """

        # Preconditions
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'classification':  # Check that the current problem type is classification.
            raise ValueError(f'Precondition: problem type of {hdlr.problem_type} is not supported')

        df = hdlr.predict()
        acc = accuracy_score(df['actual'], df['predicted'])

        return acc

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.

        :return: None
        """

        # Preconditions
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'classification':  # Check that the current problem type is classification.
            raise ValueError(f'Precondition: problem type of {hdlr.problem_type} is not supported')

        df = hdlr.predict()
        acc = accuracy_score(df['actual'], df['predicted'])

        # Display the results.
        print(f'Accuracy is {round(acc * 100, 3)}% (3 dp)')

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
        return "classification"
