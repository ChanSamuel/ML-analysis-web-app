import streamlit as st
import pages as pages
from analysers import accuracy, corr, f1, mean_std, mse, r2, shape, mae
from pages.sections import Section


def transition(options):
    """
    Transition to the next page.

    :param options: A dictionary which maps the selection box names to the analyser functions.
    """
    chosen_analysers = []
    for name in st.session_state.analyser_selection:
        chosen_analysers.append(options[name])

    st.session_state.current_page = pages.AnalysisResultsPage(chosen_analysers)


def return_action():
    """
    This is the function that is called when the 'Return to file uploader' button is pressed.
    It changes the current page to the FileUploadPage and also clears the session of any previous data.
    """
    st.session_state['current_page'] = pages.FileUploadPage()
    if 'uploaded_files' in st.session_state:
        st.session_state.uploaded_files.clear()
    if 'analyser_selection' in st.session_state:
        st.session_state.analyser_selection.clear()
    if 'hdlr' in st.session_state:
        st.session_state.hdlr = None


class AnalysisChoiceSection(Section):
    """
    This section displays 3 elements.
     - A multiselect element to select analysers with.
     - A submit button to submit the choices.
     - A back button to return to the file uploader page.
    """

    def __init__(self):
        super().__init__()
        # Create a dictionary which maps analyser names to their respective functions.
        options_keys = ['Model Accuracy', 'Correlations', 'Mean and standard deviations.', 'Shape (samples per feature)',
                        'F1 scores', 'Mean Squared Error (MSE)', 'R2 score', 'Mean Absolute Error (MAE)']
        options_values = [accuracy.AccuracyAnalyser(), corr.CorrAnalyser(), mean_std.MeanStdAnalyser(),
                          shape.ShapeAnalyser(), f1.F1Analyser(), mse.MSEAnalyser(), r2.R2Analyser(), mae.MAEAnalyser()]

        # Remove any analysis options which aren't compatible with the current model.
        # First, add all the values and keys to remove into the following lists.
        remove_values = []
        remove_keys = []
        for i in range(len(options_values)):
            if (options_values[i].model_type() != st.session_state.hdlr.problem_type) and (options_values[i].model_type() != 'agnostic'):
                remove_values.append(options_values[i])
                remove_keys.append(options_keys[i])

        # Now, remove the values and keys from the respective list.
        for i in range(len(remove_values)):
            options_values.remove(remove_values[i])
            options_keys.remove(remove_keys[i])

        self.options_dict = {}
        for idx, key in enumerate(options_keys):
            self.options_dict[key] = options_values[idx]

    def display(self):
        """
        Create a form whereby on submission, the chosen analyser names are stored in session, and a
        dictionary which maps those names to their functions, is passed to the callback function called 'transition'.
        """

        form = st.form("analyser_form")
        form.multiselect('Select below, what analysis you want done.',
                         self.options_dict.keys(),
                         key='analyser_selection')
        form.form_submit_button(on_click=transition, args=[self.options_dict])

        # Add a return button.
        cols = st.columns([1, 1, 1])
        cols[1].button('Return to file uploader', on_click=return_action)
