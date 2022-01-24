"""
The analysers package contains a collection of analyser modules.


Each analyser module provides the following:
 - An Analyser subclass.
 - Multiple analyse(Handler) methods. Each analyse method typically performs some analysis
 and returns the result of such analysis. There exists an analyse(...) function for each Handler subtype;
 multiple dispatch is used to choose the correct analyse(...) function for the corresponding Handler subtype.
 - An is_metric() method which returns whether this analyser is a performance metric or not.
 - a model_type() method which returns what model types (classification, regression, agnostic) this analyser supports.

"""

"""
The Analyser class defines the methods which all Analyser subclasses should implement.
It should be treated as an Abstract Base Class.
"""


class Analyser:

    def __init__(self):
        pass

    def analyse(self, hdlr):
        """
        Perform some analysis and return some result.
        """
        pass

    def is_metric(self):
        """
        Returns whether the result of the analysis is a performance metric or not.
        :return: True if this analyser is a metric, false otherwise.
        """
        return False

    def model_type(self):
        """
        Returns the type of model this analyser supports.
        :return: can return any of the strings: 'classification', 'regression', or 'agnostic'.
        """
        return "classification"
