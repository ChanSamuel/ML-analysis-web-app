import streamlit as st
from handlers.simple import StandardHandler
import pages as pages
from pages.sections import Section


def transition():
    model_file = None
    data_file = None

    if len(st.session_state.uploaded_files) > 2:  # Do not transition if user uploaded more than 2 files.
        st.warning('You may only upload 2 files.')
        return

    for f in st.session_state.uploaded_files:
        if f.name.endswith('.sav'):
            model_file = f
        elif f.name.endswith('.csv'):
            data_file = f
        else:
            st.error(f'File extension not recognised. File name was {f.name}')

    if model_file is None:
        st.warning('Model file not found, please upload a model file to continue.')
    elif data_file is None:
        st.warning('Dataset file not found, please upload a dataset file to continue.')
    else:
        hdlr = StandardHandler(data_file=data_file, model_file=model_file, target_idx=-1)

        # Store the handler in session.
        st.session_state.hdlr = hdlr

        # Clear the uploaded files.
        st.session_state.uploaded_files.clear()

        # Next page.
        st.session_state.current_page = pages.AnalysisChoicePage()


def submit():
    selected = st.session_state.file_selector
    if selected == 'Iris dataset: LogisticRegression':
        model_file = open('testfiles/test_model_iris.sav', 'rb')
        data_file = open('testfiles/Iris_test.csv')
    elif selected == 'Boston dataset: DecisionTreeRegressor':
        model_file = open('testfiles/test_model_boston.sav', 'rb')
        data_file = open('testfiles/Boston_test.csv')
    else:
        st.warning('Error: default model not found.')
        return

    # Store the handler in session.
    st.session_state.hdlr = StandardHandler(data_file=data_file, model_file=model_file, target_idx=-1)

    # Clear the uploaded files.
    st.session_state.uploaded_files.clear()

    # Next page.
    st.session_state.current_page = pages.AnalysisChoicePage()


class FileSection(Section):
    """
    A file Section which consists of a file uploader.
    """

    def display(self):
        comma = ', '
        allowed_files = ['.csv', '.sav']
        st.file_uploader(f'Allowed files are: {comma.join(allowed_files)}', type=allowed_files,
                         accept_multiple_files=True,
                         on_change=transition, key='uploaded_files')
        st.subheader('Or choose a sample model')
        form = st.form("file_select_form")
        form.selectbox('Choose sample model.',
                       ['Iris dataset: LogisticRegression', 'Boston dataset: DecisionTreeRegressor'],
                       key='file_selector')

        form.form_submit_button(on_click=submit)
