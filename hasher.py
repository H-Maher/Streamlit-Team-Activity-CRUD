import streamlit_authenticator as stauth



print(stauth.Hasher(["abc"]).generate())