from multimethod import multimethod

import shap

from handlers import Handler
from handlers.simple import StandardHandler
import matplotlib.pyplot as plt

# multimethod annotation is for multiple dispatch to different handler types.
from handlers.testing import TestHandler


@multimethod
def analyse(hdlr: StandardHandler):
    """
    Perform an analysis which outputs a bar plot of SHAP values for the model.
    :return: None
    """

    # Preconditions
    if hdlr is None:
        raise ValueError('Precondition: handler cannot be None')
    if hdlr.problem_type != 'classification':  # Check that the current problem type is classification.
        raise ValueError(f'Precondition: problem type of {hdlr.problem_type} is not supported')

    # Obtain the SHAP values.
    explainer = shap.explainers.Exact(hdlr.model.predict_proba, hdlr.X)
    shap_values = explainer(hdlr.X[:100])
    class_idx = 0  # An index corresponding to the target class as according to hdlr.model.classes_
    shap_values = shap_values[..., class_idx]

    # Display the results.
    shap.plots.bar(shap_values, show=False)
    plt.title(f'Mean absolute SHAP values for {hdlr.model.classes_[class_idx]}')
    plt.show()


@multimethod
def analyse(hdlr: TestHandler):
    """
    Perform an analysis which outputs a bar plot of SHAP values for the model.
    :return: None
    """

    # Preconditions
    if hdlr is None:
        raise ValueError('Precondition: handler cannot be None')
    if hdlr.problem_type != 'classification':  # Check that the current problem type is classification.
        raise ValueError(f'Precondition: problem type of {hdlr.problem_type} is not supported')

    # Obtain the SHAP values.
    explainer = shap.explainers.Exact(hdlr.model.predict_proba, hdlr.X)
    shap_values = explainer(hdlr.X[:100])
    class_idx = 0  # An index corresponding to the target class as according to hdlr.model.classes_
    shap_values = shap_values[..., class_idx]

    # Display the results.
    shap.plots.bar(shap_values, show=False)
    plt.title(f'Mean absolute SHAP values for {hdlr.model.classes_[class_idx]}')
    plt.show()


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
