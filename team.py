import streamlit as st
import datetime
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class TeamActivityForm():

    
    def __init__(self):
        self.connect_to_google_sheet()
        self.load_data()

        self.form_icon = ":mag:"

    
    def connect_to_google_sheet(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
        client = gspread.authorize(credentials)

        # Get the Google Sheet
        gsheet = client.open('Team Activity')

        try:
            
            self.activity_sheet = gsheet.worksheet('Activity Sheet')
            self.resource_sheet = gsheet.worksheet('Resource')
            self.customers_sheet = gsheet.worksheet('Customers')
            self.projects_sheet = gsheet.worksheet('Projects')
            self.task_category_sheet = gsheet.worksheet('Task Category')

        except Exception:
            st.error('Worksheet could not be found!')

    
    def load_data(self):

        # Slice from the second row to remove the column headers
        self.customers_list = self.customers_sheet.col_values(1)[1:]
        # self.projects_list = self.projects_sheet.col_values(2)[1:]
        self.projects_list = self.projects_sheet.get_all_records()[1:]
        self.task_category_list = self.task_category_sheet.col_values(1)[1:]
        self.resources_list = self.resource_sheet.col_values(1)[1:]
        self.flag = ['Yes','No']
        

    def validate_duration(self):
        if st.session_state.duration_to < st.session_state.duration_from:
            st.error('Duration can not be negative!')
            # st.session_state.duration_to = st.session_state.duration_from
                
    def generate_form(self):

        st.set_page_config(page_title='Dataplus Team Activity Form', page_icon=self.form_icon)
        st.title(self.form_icon + " " + "Welcome to Team Activity 0.1 Beta")

        with st.sidebar:
            st.button('Click Me!')


        with st.form(key='entry_form'):

            with st.container():
                col_1, col_2 = st.columns(2)

                with col_1: 
                    date = st.date_input('Date', datetime.date.today(), key='date')

                with col_2: 
                    resource = st.selectbox('Resource', self.resources_list, key='resource')

            with st.container():
                col1, col2, col3 = st.columns([1,1,1])
                
                customers_dropdown = col1.selectbox("Choose Customer", self.customers_list, key='customers_dropdown')
                project_name = col2.selectbox ('Project Name', self.projects_list, key='project_name')

                task_name = col3.text_input('Task Name', key='task_name')
                
                today_date = datetime.date.today()

            with st.container():
                col1, col2, col3 = st.columns([1,1,1])

                currentTime = datetime.datetime.now()
                durationFrom = col1.time_input('From', currentTime, key='duration_from')
                durationTo = col2.time_input('To', currentTime+datetime.timedelta(hours=1),
                                key='duration_to')
                task_category = col3.selectbox('Task Category', self.task_category_list, key='task_category')
                
            with st.container():
                col1, col2 = st.columns([2,1])

                description = col1.text_input('Description', key='description')
                billable = col2.radio("Billable", self.flag, key='billable')

            
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                self.row_entry = [st.session_state.resource, str(st.session_state.date), st.session_state.customers_dropdown, st.session_state.project_name,
                                  st.session_state.task_name, st.session_state.task_category, str(st.session_state.duration_from), str(st.session_state.duration_to),
                                  st.session_state.description, st.session_state.billable]
                
                self.validate_duration()

                self.activity_sheet.append_row(self.row_entry, value_input_option='USER_ENTERED')

                st.success('Data Submitted Successfully!')

                

             
                

                
                
              

if __name__ == "__main__":

    entry_person = TeamActivityForm()
    entry_person.generate_form()
    