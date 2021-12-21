import numpy as np
import pandas as pd
from multimethod import multimethod
from handlers import Handler
from handlers.simple import StandardHandler
from streamlit import cache
from handlers.testing import TestHandler


# cache annotation is for streamlit caching (google it).
# multimethod annotation is for multiple dispatch to different handler types (google multimethod package).
@cache
@multimethod
def analyse(hdlr: StandardHandler):
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
def analyse(hdlr: TestHandler):
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
