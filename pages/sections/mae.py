import streamlit as st
from pages.sections import Section
from analysers import mae


class MAESection(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        st.header('MAE score')

        score = mae.MAEAnalyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp

        st.metric('MAE', score)

    def fill(self, container):
        hdlr = st.session_state.hdlr

        score = mae.MAEAnalyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp

        container.metric('MAE', score)
