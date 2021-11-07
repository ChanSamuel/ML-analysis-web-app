def get_analyst_names():
    """
    Returns the formal names of all analyst methods.
    Used by Handler.unsupported_methods() to indicate which analyst methods are unsupported.
    """
    names = ['n_samples', 'n_features', 'accuracy']
    return names


class Handler:
    """
    The parent class of all Handler types. It contains methods of the form "analysistype_op()".

    These methods perform a specific analysis of the data or model (i.e., get the number of samples, check for class
    imbalance, look at the accuracy of the model, etc) and display the analysis findings.

    No class other than ModelHandler and DataHandler should directly extend this class; any subclass of Handler should
    instead extend these two classes.

    For any subclass overriding the analysis methods, the code which performs the actual analysis should be delegated
    to the respective analyst methods in the analysers package. All methods should also preferably be overridden, with
    unsupported methods raising a utilities.UnsupportedMethodException.

    At least the following pre-conditions should be checked by the corresponding analyst method:
     - If the problem type (classification or regression) of this Handler is suitable for this analysis.
     - If any additional handlers passed as parameters are of the correct implementation.

    """

    def __init__(self):
        """This constructor does nothing, subclasses are expected to implement this."""
        pass

    def unsupported_methods(self):
        """
        Returns the list of unsupported analysts/methods.
        The elements of the returned list are the Analyst.name() of the corresponding analysis method.

        :return: the list of unsupported Analyst names.
        """
        raise NotImplementedError('unsupported_methods must be overridden!')

    def n_samples_op(self):
        """
        Perform an analysis to return the number of samples in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('n_samples_op must be overridden!')

    def n_features_op(self):
        """
        Perform an analysis to return the number of features in the data.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('n_features_op must be overridden!')

    def accuracy_op(self):
        """
        Perform an analysis to return the accuracy in the model.
        This method should only work for classification models.
        This method will throw an exception if either not overridden by a subclass or super() is called.

        :return: None
        """
        raise NotImplementedError('accuracy_op must be overridden!')
