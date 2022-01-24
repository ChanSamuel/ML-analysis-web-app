import streamlit as st

from pages.sections import Section
from mappings import analyser_to_section
from pages.sections.f1 import F1Section
from analysers.f1 import F1Analyser


class MetricsSection(Section):
    """
    MetricsSection is constructed with a list of chosen_analysers, these analysers should be considered a metric
    (i.e., Analyser::is_metric should return true).
    The sections corresponding to these analysers are then found and stored.
    Upon calling MetricSection::display(), a container for each metric is created, these containers are displayed in
    rows of 3. The fill(container) method of each section is called to fill each container with their
    respective content.
    """

    def __init__(self, chosen_analysers):
        super().__init__()
        self.f1_sec = None
        self.sections = []
        for analyst in chosen_analysers:
            self.sections.append(analyser_to_section(analyst))

    def display(self):
        st.header("Metrics")

        # Firstly, if there is an F1 section specified, find it and remove it from the sections list
        # so that it can be treated separately from the rest of the metrics.
        for i in range(len(self.sections)):
            if isinstance(self.sections[i], F1Section):
                self.f1_sec = self.sections[i]
                self.sections.remove(self.f1_sec)
                break

        # Now, display the sections in rows of 3.
        nrows = len(self.sections) // 3
        remainder = len(self.sections) % 3

        # First, display the full rows.
        idx = 0
        for i in range(nrows):
            cols = st.columns(3)
            for col in cols:
                self.sections[idx].fill(col)
                idx += 1

        # Then, display the last remaining non-full row (if it exists).
        if remainder > 0:  # Check that there is atleast one remaining metric section to display on a new row.
            cols = st.columns(3)
            for j in range(remainder):
                self.sections[idx].fill(cols[j])
                idx += 1

        # Now, we display the f1 section if it exists. If not, we return.
        if self.f1_sec is None:
            return

        # If the F1 score is a single number (rather than a table) AND there are spaces left in the last remainder row.
        # then, we can fill up the remaining spot with an F1 score metric.

        # Check if the model is a binary classifier, if so then the F1 analysis will return a single score rather than
        # a score for each class.
        if len(st.session_state.hdlr.model.classes_) == 2:
            # Check that there is a remaining space in the last remainder row.
            if remainder == 1:
                # There are 2 remaining spaces so fill the next one up.
                next_space = 1
            elif remainder == 2:
                # There is 1 space left, so fill that one up.
                next_space = 2
            else:
                # There are 0 spaces left, so we must display them on new rows.
                self.f1_sec.display()
                return
            f1_score = round(F1Analyser().analyse(st.session_state.hdlr), 3)
            cols[next_space].metric('F1 score', f1_score)
            return

        # There are multiple classes, so the F1 scores need to be displayed on new rows.
        self.f1_sec.display()
