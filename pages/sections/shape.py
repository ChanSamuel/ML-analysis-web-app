from pages.sections import Section
from analysers import shape, show_data
import streamlit as st


class ShapeSection(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        # Unpack the output from the analyser.
        packed = shape.ShapeAnalyser().analyse(hdlr)
        nrows = packed[0]
        ncols = packed[1]
        samples_per_feature = packed[2]
        if len(packed) > 3:  # If it exists (i.e., the model is a classifier) unpack the 4th value.
            n_classes = packed[3]

        st.header("Shape")

        # If classification, then also display the number of classes as a metric.
        if len(packed) > 3:
            cols = st.columns(4)
            cols[0].metric('Number of samples', nrows)
            cols[1].metric('Number of features', ncols)
            cols[2].metric('Samples per feature', samples_per_feature)
            cols[3].metric('Number of classes', n_classes)
        else:
            cols = st.columns(3)
            cols[0].metric('Number of samples', nrows)
            cols[1].metric('Number of features', ncols)
            cols[2].metric('Samples per feature', samples_per_feature)

        # Show the data as a table underneath.
        tbl = show_data.ShowDataAnalyser().analyse(hdlr)
        st.dataframe(tbl)
