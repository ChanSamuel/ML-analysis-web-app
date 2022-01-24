from pages.sections import Section
import streamlit as st


class InitialHeaderSection(Section):
    """
    A header Section which consists of a title and subtitle.
    """

    def display(self):
        st.title('Sklearn Model Analyser')
        st.subheader('Step 1: Upload a Pickled Sklearn Model and dataset.')


class AnalysisHeaderSection(Section):
    def display(self):
        st.title('Sklearn Model Analyser')
        st.subheader('Step 2: Choose your analysis types.')
