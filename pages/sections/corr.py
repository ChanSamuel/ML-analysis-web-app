import streamlit as st

from pages.sections import Section
from analysers import corr


class CorrSection(Section):

    def display(self):
        hdlr = st.session_state.hdlr

        tbl, strong_corrs = corr.CorrAnalyser().analyse(hdlr)

        st.header('Correlations')

        corr_list = st.expander('Open to see the list of strong correlations.')
        corr_list.subheader('Strong correlations (>0.7):')

        for i, key in enumerate(strong_corrs.keys()):
            rounded_corr = round(strong_corrs[key], 3)
            corr_list.metric(label=key, value=rounded_corr)

        st.subheader('Correlation table')
        st.dataframe(tbl)
