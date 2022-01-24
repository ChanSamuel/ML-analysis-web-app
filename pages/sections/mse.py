import streamlit as st
from analysers.mse import MSEAnalyser


class MSESection:

    def display(self):
        hdlr = st.session_state.hdlr

        st.header('MSE')

        score = MSEAnalyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp.

        st.metric('Mean Squared Error (MSE)', score)

    def fill(self, container):
        hdlr = st.session_state.hdlr

        score = MSEAnalyser().analyse(hdlr)
        score = round(score, 3)  # Round to 3dp.

        container.metric('Mean Squared Error (MSE)', score)
