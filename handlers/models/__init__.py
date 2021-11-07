from handlers import Handler
from handlers.utilities import UnsupportedMethodException


class ModelHandler(Handler):
    """
    The parent abstract class for all ModelHandlers.
    This class is designed to be used as an interface, thus it has no implementation.
    ModelHandler loads in a given model file, and has several unimplemented analysis methods.
    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        super().__init__()

    def load_model(self, file):
        """Load and return the file as a model in some format."""
        raise NotImplementedError('load_model must be overridden!')

    def predict(self, data):
        """
        Return the predictions for each datapoint using the stored model in this ModelHandler.
        Should return a dataframe with a column for the actual target labels, and a column for the predicted
        target labels.
        """
        raise NotImplementedError('predict must be overridden!')

    def predict_proba(self, data):
        """
        Return the prediction probabilities using the stored model in this ModelHandler.
        May not necessarily be supported by the subclass implementation.
        """
        raise NotImplementedError('predict_proba must be overridden!')

    def unsupported_methods(self):
        """
        Returns the list of unsupported analysts/methods.
        The names in the returned list are the names based off of models.get_analyst_names()

        :return: the list of unsupported Analyst names.
        """
        raise NotImplementedError('unsupported_methods must be overridden!')

    def n_samples_op(self):
        """
        This method is not supported by ModelHandler; calling will result in UnsupportedMethodException
        """
        raise UnsupportedMethodException('n_samples analysis is not supported for ModelHandler, ' 
                                         'use DataHandler instead')

    def n_features_op(self):
        """
        This method is not supported by ModelHandler; calling will result in UnsupportedMethodException
        """
        raise UnsupportedMethodException('n_samples analysis is not supported for ModelHandler, ' 
                                         'use DataHandler instead')

    def accuracy_op(self):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('not yet developed')
