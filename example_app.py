import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('My app')

if 'count' not in st.session_state:
    st.session_state['count'] = 0

if st.button('a button'):
    st.session_state.count += 1
    st.write(f'Button has been clicked {st.session_state.count} times.')
else:
    st.write('Button has yet to be clicked.')

n_iterations = 5
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['col1', 'col2', 'col3'])

col1, col2 = st.columns([3, 1])
with col1:
    st.header('Line chart')
    lc = st.line_chart(chart_data)

with col2:
    st.header('Data')
    data_table = st.dataframe(chart_data)
with st.empty():
    for i in range(n_iterations):
        new_rows = pd.DataFrame(
            np.random.randn(1, 3),
            columns=['col1', 'col2', 'col3'])
        lc.add_rows(new_rows)
        data_table.add_rows(new_rows)

        st.write(f"⏳ {i} seconds have passed")
        time.sleep(1)

    st.write("✔️ 5 seconds over!")

