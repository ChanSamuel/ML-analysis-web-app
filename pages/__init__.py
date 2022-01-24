"""
This package contains a collection of Page classes and Section classes.
The purpose of this package is to allow external app modules to construct these Pages into objects and then display
their content, and assign transitions to different pages.

A description of what a 'Page' is:

A Page is simply a class which contains the content to display to the user's screen.
It contains a list of Sections (see pages.sections) which each can be displayed using the Section::display() method.

Whenever a change is detected (and upon initialization),
app.py will grab the current Page from the session state and call this method for each Section.

"""
from mappings import analyser_to_section
from pages.sections.metrics import MetricsSection
from pages.sections.analysis_choice import AnalysisChoiceSection
from pages.sections.file_uploader import FileSection
from pages.sections.headers import InitialHeaderSection, AnalysisHeaderSection


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


class FileUploadPage(Page):
    """
    The page after the initial page.
    It consists of a header, and a file section.
    """
    def __init__(self):
        super(FileUploadPage, self).__init__()
        self.sections = [InitialHeaderSection(), FileSection()]


class AnalysisChoicePage(Page):
    """
    The page after the initial page.
    It consists of a header, and a section for analysis choice.
    """

    def __init__(self):
        super(AnalysisChoicePage, self).__init__()
        self.sections = [AnalysisHeaderSection(), AnalysisChoiceSection()]


class AnalysisResultsPage(Page):
    """
    The page where the analysis results are shown.
    It consists of a header, an analysis choice section, and the results of the analysis.
    """

    def __init__(self, chosen_analysers):
        """
        Construct the analysis results page.

        :param chosen_analysers: a list of analyser functions from the analysers package, these are the
        analysers the user has chosen.

        """
        super(AnalysisResultsPage, self).__init__()

        # Separate the analysers from metrics and non metrics.
        metrics = []
        non_metrics = []
        for analyser in chosen_analysers:
            if analyser.is_metric():
                metrics.append(analyser)
            else:
                non_metrics.append(analyser)

        self.sections = [AnalysisHeaderSection(), AnalysisChoiceSection()]
        if len(metrics) > 0:
            self.sections.append(MetricsSection(metrics))

        for analyst in non_metrics:
            self.sections.append(analyser_to_section(analyst))


