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
    Calculate and return the correlation table between features as a dataframe.
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
            if i != j:  # Skip comparisons between same features.
                r = abs(corr_tbl.iloc[i, j])  # Take the strength of the correlation.

                # If the correlation is stronger or equal to 0.7, consider it to be strong.
                if r >= 0.7:
                    key = str(tbl.columns[i]) + ' & ' + str(tbl.columns[j])
                    strong_corrs[key] = r

    # Return the correlation table as well as any strong correlations as a dictionary.
    return corr_tbl, strong_corrs


@multimethod
def analyse(hdlr: TestHandler):
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
            if i != j:  # Skip comparisons between same features.
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
