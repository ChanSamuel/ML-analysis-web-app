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
    Perform an analysis to get the number of samples, features, and the ratio between the samples and features in the data.
    If the problem_type is classification, then this method will also return the number of classes.
    This method will throw an exception if either not overridden by a subclass or super() is called.

    :returns: Either a tuple (n_samples, n_features, samples_per_feature) OR a tuple (n_samples, n_features, samples_per_feature, n_classes)
    """

    # Pre-condition checks.
    if hdlr.data is None:
        raise ValueError('Precondition: self.data is None')
    if not (hdlr.problem_type in ['classification', 'regression']):  # Check that the current problem type is valid.
        raise ValueError(f'Precondition: problem_type of {hdlr.problem_type} is not supported')

    # Obtain the number of rows and columns.
    nrows = hdlr.data.shape[0]
    ncols = hdlr.data.shape[1]

    # Calculate the samples to feature ratio
    samples_per_feature = round(nrows / ncols, 2)

    # If doing a classification problem also return the number of classes.
    if hdlr.problem_type == 'classification':
        nclasses = len(hdlr.y.unique())
        return nrows, ncols, samples_per_feature, nclasses
    else:
        return nrows, ncols, samples_per_feature


@multimethod
def analyse(hdlr: TestHandler):
    """
    Perform an analysis to get the number of samples and features in the data.
    If the problem_type is classification, then this method will also analyse number of classes.
    This method will throw an exception if either not overridden by a subclass or super() is called.

    :return: None
    """

    # Pre-condition checks.
    if hdlr.data is None:
        raise ValueError('Precondition: self.data is None')
    if not (hdlr.problem_type in ['classification', 'regression']):  # Check that the current problem type is valid.
        raise ValueError(f'Precondition: problem_type of {hdlr.problem_type} is not supported')

    # Obtain the number of rows and columns.
    nrows = hdlr.data.shape[0]
    ncols = hdlr.data.shape[1]

    # Now we print the results.

    # If doing a classification problem also print the number of classes.
    if hdlr.problem_type == 'classification':
        nclasses = len(hdlr.y.unique())
        print(f'Data has {nrows} samples, {ncols} features (including target feature), and {nclasses} classes.')
    else:
        print(f'Data has {nrows} samples, {ncols} features (including target feature).')

    # Additionally, print out the number of samples per feature.
    samples_per_feature = round(nrows / ncols, 2)
    if samples_per_feature < 5:
        print(f'There are {samples_per_feature} samples per feature. Consider increasing the number of samples '
              f'or decreasing the number features.')
    else:
        print(f'There are {samples_per_feature} samples per feature.')


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
