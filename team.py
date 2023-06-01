import streamlit as st
import datetime
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class TeamActivityForm():

    def __init__(self):
        self.team_activity_sheet = self.connect_to_google_sheet()
        
        self.activity_sheet = self.load_data('Activity Sheet')
        self.resources_list = self.load_data('Resource').col_values(1)[1:]
        self.customers_list = self.load_data('Customers').col_values(1)[1:]
        self.projects_sheet = self.load_data('Projects').get_all_records()[1:]
        self.projects_list = pd.DataFrame(self.projects_sheet)
        self.task_category_list = self.load_data('Task Category').col_values(1)[1:]
        
        self.flag = ['Yes','No']

    @st.cache_resource
    def connect_to_google_sheet(_self):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
        client = gspread.authorize(credentials)

        # Get the Google Sheet
        gsheet = client.open('Team_Activity')

        return gsheet

    @st.cache_resource
    def load_data(_self, selected_gsheet):
        return _self.team_activity_sheet.worksheet(selected_gsheet)


    def generate_form(self):

        st.title(":mag: Welcome to Dataplus Team Activity Form")

        def __prepare_entry_row():
            st.session_state.duration_from = st.session_state.duration_from
            st.session_state.duration_to = st.session_state.duration_to


        with st.sidebar:
            st.image('https://www.dataplusme.com/images/logo/alogo.jpg')
            st.button('Click Me!')

        with st.container():
            col1, col2, col3 = st.columns([1,1,1])

            today_date = datetime.date.today()
            date = col1.date_input('Date', today_date, key='date')
            resource = col2.selectbox('Resource', self.resources_list, key='resource')
            customers_dropdown = col3.selectbox("Choose Customer", self.customers_list, key='customers_dropdown')
            
            filtered_projects = self.projects_list[self.projects_list['Customer'] == st.session_state.customers_dropdown]['Project Name']

        with st.form(key='entry_form', clear_on_submit=True):

            with st.container():
                col1, col2 = st.columns([1,1])

                project_name = col1.selectbox ('Project Name', options=filtered_projects, key='project_name')
                task_name = col2.text_input('Task Name', key='task_name')


            with st.container():
                col1, col2, col3 = st.columns([1,1,1])

                currentTime = datetime.datetime.now()
                durationFrom = col1.time_input('From', key='duration_from')
                durationTo = col2.time_input('To', key='duration_to')
                task_category = col3.selectbox('Task Category', self.task_category_list, key='task_category')
                
            with st.container():
                col1, col2 = st.columns([2,1])

                description = col1.text_input('Description', key='description')
                billable = col2.radio("Billable", self.flag, key='billable')

            
            submit_button = st.form_submit_button("Submit", on_click=__prepare_entry_row)


            if submit_button:

                prepared_entry_row = [st.session_state.resource, str(st.session_state.date), st.session_state.customers_dropdown,
                                      st.session_state.project_name, st.session_state.task_name, st.session_state.task_category,
                                      str(st.session_state.duration_from), str(st.session_state.duration_to),
                                      st.session_state.description, st.session_state.billable]

                self.activity_sheet.append_row(prepared_entry_row, value_input_option='USER_ENTERED')

                st.success('Data Submitted Successfully!')

        st.columns([1,3,1])[1].header('If you like the developers, please consider supporting us with :heavy_dollar_sign:**5** at our desk:sunglasses:. Thanks!')


if __name__ == "__main__":

    form_icon = ":mag:"
    st.set_page_config(page_title='Dataplus Team Activity Form', page_icon=form_icon, layout='wide')

    entry_person = TeamActivityForm()
    entry_person.generate_form()
    