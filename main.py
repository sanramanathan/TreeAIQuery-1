# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions.utility import check_password
import leafmap.foliumap as leafmap

APP_TITLE = 'TreeAI Querry'
APP_SUB_TITLE = 'Geospatial AI Assiatant for NParks Trees and Species data'


#st.title(APP_TITLE)
#st.caption(APP_SUB_TITLE)
#st.set_page_config(layout="wide")
#st.set_page_config(APP_TITLE)

def main():

 #region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="wide",
        page_title=APP_TITLE
    )
# endregion <--------- Streamlit App Configuration --------->
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    row1_col1, row1_col2 = st.columns([3, 1.3])
    width = None
    height = 600
    layers = None

    # Load basemaps
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenStreetMap")



    #display prompt
    with row1_col2:
        basemap = st.selectbox("Select a basemap:", options, index)

        form = st.form(key="form")
        form.subheader("Prompt")
        user_prompt = form.text_area("Enter your prompt here", height=200)
        if form.form_submit_button("Submit"):
            st.toast(f"User Input Submitted - {user_prompt}")
            st.divider()
            response= user_prompt
            st.write(response)
            st.divider()

    #display map
    with row1_col1:
       #Leaf Map

        m = leafmap.Map(center=[1.352083, 103.819836], zoom=11)
        m.add_basemap(basemap)
        m.to_streamlit(width, height)
    
if __name__ == "__main__":
    # Check if the password is correct.  
    if not check_password():
        st.stop()
    main()