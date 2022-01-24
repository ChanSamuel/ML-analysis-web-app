from matplotlib import pyplot as plt

from pages.sections import Section
from analysers import mean_std

import streamlit as st


class MeanStdSection(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        st.header('Mean and Standard deviations')

        tbl = mean_std.MeanStdAnalyser().analyse(hdlr)
        st.dataframe(tbl)  # Display the table as a dataframe element.

        # Plot the means of each feature as a bar chart.
        fig, ax = plt.subplots(figsize=(8, 3))
        feature_names = tbl.columns
        means = tbl.iloc[0, ::]
        ax.set_title('Mean averages of each feature.')
        ax.set_ylabel('Mean')
        ax.bar(feature_names, means, color='red')

        st.pyplot(fig)

        # Plot the standard deviations of each feature as a bar chart.
        fig, ax = plt.subplots(figsize=(8, 3))
        feature_names = tbl.columns
        stdevs = tbl.iloc[1, ::]
        ax.set_title('Standard deviations of each feature.')
        ax.set_ylabel('Standard deviation')
        ax.bar(feature_names, stdevs, color='green')

        st.pyplot(fig)
