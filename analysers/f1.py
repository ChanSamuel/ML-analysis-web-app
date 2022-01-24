import pandas as pd
from multimethod import multimethod
from sklearn.metrics import f1_score
from analysers import Analyser
from handlers.simple import StandardHandler
from handlers.testing import TestHandler
from exceptions import UnsupportedMethodException
from streamlit import cache


class F1Analyser(Analyser):

    # cache annotation is for streamlit caching (google it).
    # multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
    @multimethod
    @cache
    def analyse(self, hdlr: StandardHandler):
        """
        Calculate and return the f1 score(s) for the current model.
        If current model is multi-class, then the F1-score for each class will be returned as a dataframe.
        Raises UnsupportedMethodException if current model is not a classification model.

        :raises: UnsupportedMethodException
        :returns: a score between 0 and 1, or a dataframe of shape [1, c] where c is the number of classes.
        """

        # Preconditions.
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'classification':
            raise UnsupportedMethodException('F1 score cannot be used on non-classification model.')

        # Give the f1 scores for each class if not binary classification.
        if len(hdlr.model.classes_) == 2:
            score = f1_score(hdlr.y, hdlr.model.predict(hdlr.X))
            return score
        else:
            scores = f1_score(hdlr.y, hdlr.model.predict(hdlr.X), average=None)
            score_table = pd.DataFrame(columns=hdlr.model.classes_)
            score_table.loc[0] = scores
            return score_table

    @multimethod
    def analyse(self, hdlr: TestHandler):
        """
        Calculate the f1 score(s) for the current model.
        If current model is multi-class, then the F1-score for each class will be shown.
        Raises UnsupportedMethodException if current model is not a classification model.

        :raises: UnsupportedMethodException
        """

        # Preconditions.
        if hdlr is None:
            raise ValueError('Precondition: handler cannot be None')
        if hdlr.problem_type != 'classification':
            raise UnsupportedMethodException('F1 score cannot be used on non-classification model.')

        # Give the f1 scores for each class if not binary classification.
        if len(hdlr.model.classes_) == 2:
            score = f1_score(hdlr.y, hdlr.model.predict(hdlr.X))
            print('The F1 score is:', score)
        else:
            scores = f1_score(hdlr.y, hdlr.model.predict(hdlr.X), average=None)
            score_table = pd.DataFrame(columns=hdlr.model.classes_)
            score_table.loc[0] = scores
            print('The F1 scores for each class are:')
            print(score_table)

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
