from handlers.models import ModelHandler


class SklearnModelHandler(ModelHandler):
    """
    Is able to load in a pickled sklearn model from a file.
    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        super().__init__()

    def load_model(self, file):
        """Load and return the file as a model in some format."""
        raise NotImplementedError('not yet developed')

    def predict(self, data):
        """Return the predictions for each datapoint using the stored model in this ModelHandler."""
        raise NotImplementedError('not yet developed')

    def predict_proba(self, data):
        """
        Return the prediction probabilities using the stored model in this ModelHandler.
        May not necessarily be supported by the subclass implementation.
        """
        raise NotImplementedError('not yet developed')

    def unsupported_methods(self):
        """
        Returns the list of unsupported analysts/methods.
        The names in the returned list are the names based off of models.get_analyst_names()

        :return: the list of unsupported Analyst names.
        """
        raise NotImplementedError('unsupported_methods must be overridden!')

    def accuracy_op(self):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('accuracy_op must be overridden!')
