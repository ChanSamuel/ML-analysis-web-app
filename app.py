import streamlit as st
import pages as pages

# Initialise the current page if using fresh session.
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = pages.InitialPage()

# Display the page by displaying each of its sections.
for segment in st.session_state['current_page']:
    segment.display()
