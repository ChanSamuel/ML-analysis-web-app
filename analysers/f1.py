import pandas as pd
from multimethod import multimethod
from sklearn.metrics import f1_score

from handlers import Handler
from handlers.simple import StandardHandler
from handlers.exceptions import UnsupportedMethodException


# multimethod annotation is for multiple dispatch to different handler types.
from handlers.testing import TestHandler


@multimethod
def analyse(hdlr: StandardHandler):
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


@multimethod
def analyse(hdlr: TestHandler):
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


def supported_handlers():
    """
    Returns the list of handler types which have been implemented by this module.
    Should return the types of what analyse() methods exist for what Handler types;

    i.e., if the methods analyse(hdlr: StandardHandler), and analyse(hdlr: TestHandler) have
    been implemented in this module, then the returned list is [StandardHandler, TestHandler].

    The returned list should never contain the Handler class itself.

    :return: supported: [StandardHandler, TestHandler]
    """
    return [StandardHandler, TestHandler]


def supports(hdlr: Handler):
    """
    Check if the given handler is supported by this analysis or not.
    Returns false if this module has no analyse() function corresponding to this handler type,
    true otherwise. I.e., if this hdlr's class is not contained in supported_handlers().

    :param hdlr:
    :return: false if this module has no analyse() function corresponding to this handler type.
    """

    # Preconditions
    if hdlr is None:
        raise ValueError('hdlr cannot be None.')
    if not isinstance(hdlr, Handler):
        raise ValueError('Given hdlr is not a subclass of Handler.')

    for clazz in supported_handlers():
        if isinstance(hdlr, clazz):
            return True

    return False
