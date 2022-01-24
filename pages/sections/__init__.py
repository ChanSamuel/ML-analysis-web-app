"""
This package contains a collection of Section classes.
Sections are just a section of content that can be displayed on the screen.
When put together, Sections make up a 'Page' of content.
"""


class Section:
    """
    Each Section has a display() method which displays its content to the page.
    If the particular section displays a metric, then it should implement a fill(container) method which takes
    in a streamlit container and displays its content inside that container rather than on the page. This fill()
    method will be used rather than display().
    """

    def __init__(self):
        """
        Does nothing.
        Subclasses are expected to provide their own parameters to construct with.
        """
        pass

    def display(self):
        """
        Displays this Section's content on screen.
        If not implemented by a subclass, this will throw an exception.
        """
        raise NotImplementedError('Page::display must be overridden!')
