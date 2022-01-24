import streamlit as st
from pages.sections import Section
from analysers import r2


class R2Section(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        st.header('R2 score')

        score = r2.R2Analyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp

        st.metric('R2', score)

    def fill(self, container):
        hdlr = st.session_state.hdlr

        score = r2.R2Analyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp

        container.metric('R2', score)
