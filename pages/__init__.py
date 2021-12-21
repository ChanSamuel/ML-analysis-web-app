"""
This package contains a collection of Page classes and Section classes.
The purpose of this package is to allow external app modules to construct these Pages into objects and then display
their content, and assign transitions to different pages.

Anything outside this package should not need to worry about sections.

A description of what a 'Page' is:

A Page is simply a class which contains the content to display to the user's screen.
It contains a list of Sections (see pages.sections) which each can be displayed using the Section::display() method.

Whenever a change is detected (and upon initialization),
app.py will grab the current Page from the session state and call this method for each Section.

"""
from pages.sections.file_uploader import FileSection
from pages.sections.header import HeaderSection


class Page:
    """
    The parent class of all pages.
    Has no functionality, we just use this to make all page implementations have a subclass relation with this Page.
    """
    def __init__(self):
        """
        Does nothing.
        """
        pass


class InitialPage(Page):
    """
    The very first page the user sees on a fresh session.
    It has a header section, and a file section.
    """
    def __init__(self):
        super(InitialPage, self).__init__()
        self.sections = [HeaderSection(), FileSection()]
