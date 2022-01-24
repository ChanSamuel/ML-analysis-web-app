from analysers import f1
from pages.sections import Section
import streamlit as st


class F1Section(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        # NOTE: this method will only be called if the model is not a binary classifier.
        # If the model IS a binary classifier, then refer to pages.sections.metrics module for the implementation.

        f1_tbl = f1.F1Analyser().analyse(hdlr)
        classes = f1_tbl.columns

        # Now, we loop through and display the f1 score for each class.
        # We display them side-by-side in rows of 3.
        col_idx = 0
        cols = st.columns(3)
        for i in range(len(classes)):
            score = round(f1_tbl.iloc[0, i], 3)
            name = f'F1: {classes[i]}'

            cols[col_idx].metric(name, score)

            col_idx += 1

            # Reset the column index to 0 once we reach 3, then create a new row of columns.
            # However, do not do this if we are on the last iteration.
            if (col_idx == 3) and ((i+1) != len(classes)):
                cols = st.columns(3)
                col_idx = 0
