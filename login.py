import streamlit as st
import streamlit_authenticator as stauth
from team import TeamActivityForm

import yaml
from yaml.loader import SafeLoader
with open('./security/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


# st.set_page_config(page_title='Dataplus Team Activity Form', page_icon=form_icon, layout='wide')

name, authentication_status, username = authenticator.login('Login', 'main')

# # Forget Password Block
# try:
#     username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
#     if username_forgot_pw:
#         st.success('New password sent securely')
#         # Random password to be transferred to user securely
#     else:
#         st.error('Username not found')
# except Exception as e:
#     st.error(e)

# # Register New User
# try:
#     if authenticator.register_user('Register user', preauthorization=False):
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)

# Login Block
if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    st.title('Some content')

    entry_person = TeamActivityForm()
    entry_person.generate_form()
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')

# # Reset Password Block
# if authentication_status:
#     try:
#         if authenticator.reset_password(username, 'Reset password'):
#             with open('./security/config.yaml', 'w') as file:
#                 yaml.dump(config, file, default_flow_style=False)
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)