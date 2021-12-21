"""
This package contains a collection of Section classes.
Sections are just a section of content that can be displayed on the screen.
When put together, Sections make up a 'Page' of content.
"""


class Section:
    """
    A Section does the following:
     - Is constructed with a certain set of parameters which it stores as fields.
     - Raises an exception if the given parameters are invalid.
     - Uses said fields to display it's content.
    """

    def __init__(self):
        """
        Does nothing.
        Subclasses are expected to provide their own parameters to construct with, and throw an exception if
        the passed parameters are not correct.
        """
        pass

    def display(self):
        """
        Displays this Section's content on screen.
        If not implemented by a subclass, this will throw an exception.
        """
        raise NotImplementedError('Page::display must be overridden!')
