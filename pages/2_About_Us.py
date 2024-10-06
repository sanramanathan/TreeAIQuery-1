import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="TreeAI Query Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("TreeAI Query")

st.write("This is a Streamlit App that demonstrates how to use the OpenAI API to generate text completions.")

with st.expander("How to use this App"):
    st.write("1. Enter your prompt in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a text completion based on your prompt.")
