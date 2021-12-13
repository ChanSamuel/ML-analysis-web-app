from multimethod import multimethod
from sklearn.metrics import mean_squared_error

from handlers import Handler
from handlers.exceptions import UnsupportedMethodException
from handlers.simple import StandardHandler


# multimethod annotation is for multiple dispatch to different handler types.
@multimethod
def analyse(hdlr: StandardHandler):
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


def supported_handlers():
    """
    Returns the list of handler types which have been implemented by this module.
    Should return the types of what analyse() methods exist for what Handler types;

    i.e., if the methods analyse(hdlr: StandardHandler), and analyse(hdlr: TestHandler) have
    been implemented in this module, then the returned list is [StandardHandler, TestHandler].

    The returned list should never contain the Handler class itself.

    :return: supported: [StandardHandler]
    """
    return [StandardHandler]


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
