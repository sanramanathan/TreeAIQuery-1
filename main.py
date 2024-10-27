# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions.utility import check_password
import leafmap.foliumap as leafmap
import geopandas as gpd
#import geopy
import requests
import json
import plotly.express as px
import geojson

from logics.user_query_handler import process_user_message

#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter

def load_data(data):
    return pd.read_csv(data)


APP_TITLE = 'TreeAI Query'
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
    #options = list(leafmap.basemaps.keys())
    #index = options.index("OpenStreetMap")

    treessg =  load_data("https://raw.githubusercontent.com/sanramanathan/dataAIBootCAMP/refs/heads/main/trees_1000000.csv")
    df =  treessg

    #display prompt
    with row1_col2:
        #basemap = st.selectbox("Select a basemap:", options, index)

        #street = st.sidebar.text_input("Street", "Clementi Avenue 5")
        #region = st.sidebar.text_input("Region", "Singapore")
        #country = st.sidebar.text_input("Country", "Singapore")

        #geolocator = Nominatim(user_agent="GTA Lookup")
        #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        #location = geolocator.geocode(street+", "+region+", "+country)

        #lat = location.latitude
        #lon = location.longitude


        #_lat =[]
        #_lon = []

        #url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal=120344&returnGeom=Y&getAddrDetails=Y&pageNum=1"    
        #response = requests.request("GET", url)    
        #print(response.text)
        #st.toast(f"User Input Submitted - {response.text}")
        
        #response_dict = json.loads(response.content)
        #type(response_dict)

        #if response_dict["found"] != 0:
           # _lat.append(response_dict["results"][0]["LATITUDE"])
            #_lon.append(response_dict["results"][0]["LONGITUDE"])
            #m = leafmap.Map(center=[response_dict["results"][0]["LATITUDE"], response_dict["results"][0]["LONGITUDE"]], zoom=5)
       

        form = st.form(key="form")
        form.subheader("Prompt")
        user_prompt = form.text_area("Enter your prompt here", height=200)
        if form.form_submit_button("Submit"):
            #st.toast(f"User Input Submitted - {user_prompt}")
            st.divider()
            if user_prompt != "":
                response , trees_infos = process_user_message(user_prompt)
                st.write(response)
                st.divider()
                df2 = pd.DataFrame(trees_infos)          
                df = df2

            else:
                response ="Please provide valid query"
                st.write(response)
                
            





    #display map
    with row1_col1:
        
 
        

        # dropdown
        #species_list = treessg["species_id"].unique().tolist()
        #selected_species = st.sidebar.selectbox("species_id",species_list)


        #with st.expander("TreesSG data"):
            
            #st.dataframe(df)
            #st.dataframe(treessg)
        
        # plot all treessg
        fig = px.scatter_mapbox(df , lat="lat",lon="lng",hover_name="tree_id",hover_data=["species_id","girth","height","age"],
                                color_discrete_sequence= ["green"],zoom=10, height= 700,size_max=50
                                )
        subzones = "./data/MasterPlan2019SubzoneBoundaryNoSeaGEOJSON.geojson"

        fig.update_layout(mapbox_style="open-street-map")
        
        with open(subzones) as f:
            gj = geojson.load(f)

        fig.update_layout(mapbox_layers=[{
                    "name": "SubZones",
                    "below": 'traces',
                    "sourcetype": "geojson",
                    "type": "line",
                    "color": "brown",
                    "source": gj
                }])

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig)
 
 
 
 
 
 
 
       #Leaf Map

        #m = leafmap.Map(center=[1.352083, 103.819836], zoom=11)

        #m = leafmap.Map(center=[1.31812073993323 ,103.769088401723], zoom=1)
        #m.add_basemap(basemap)
        #regions = "./data/MasterPlan2019SubzoneBoundaryNoSeaGEOJSON.geojson"
        #m.add_geojson(regions, layer_name="MP2019 Subzones")
        #m.to_streamlit(width, height)
            
        with st.expander("Disclaimer"):
            st.write(
                    """

                    IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

                    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

                    Always consult with qualified professionals for accurate and personalized advice.

                    """

            )
            st.image("https://static.streamlit.io/examples/dice.jpg")
    
if __name__ == "__main__":
    # Check if the password is correct.  
    if not check_password():
        st.stop()
    main()