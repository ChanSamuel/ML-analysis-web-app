from pages.sections import Section
from analysers import accuracy
import streamlit as st


class AccuracySection(Section):
    """
    Display the accuracy as a single streamlit metric element.
    """

    def display(self):
        hdlr = st.session_state.hdlr

        st.header('Accuracy')

        acc = accuracy.AccuracyAnalyser().analyse(hdlr)
        acc = round(acc, 3) * 100  # Round to 3dp and convert to percentage.

        st.metric('Accuracy', f'{acc}%')

    def fill(self, container):
        hdlr = st.session_state.hdlr

        acc = accuracy.AccuracyAnalyser().analyse(hdlr)
        acc = round(acc, 3) * 100  # Round to 3dp and convert to percentage.

        container.metric('Accuracy', f'{acc}%')
