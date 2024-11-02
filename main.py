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


#from logics.user_query_handler import process_user_message
from logics.user_query_handler import get_response_custom_agent
from logics.user_query_handler import get_response_retrieverFFW
from langchain_core.messages import AIMessage, HumanMessage

def load_data(data):
    return pd.read_csv(data)


APP_TITLE = 'TreeAI Query'
APP_SUB_TITLE = 'Geospatial AI Assiatant for NParks Trees and Species data'



def main():

 #region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="wide",
        page_title=APP_TITLE
    )
# endregion <--------- Streamlit App Configuration --------->
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # row1_col1, row1_col2 = st.columns([2, 1.3])
    # width = None
    # height = 600
    # layers = None

    # Load basemaps
    #options = list(leafmap.basemaps.keys())
    #index = options.index("OpenStreetMap")

    treessg =  load_data("https://raw.githubusercontent.com/sanramanathan/dataAIBootCAMP/refs/heads/main/trees_1000000.csv")
    df =  treessg


    #display prompt
    # with row1_col2:

    label = "Type exit to discontinue and start a new one "

    s = f"<p style='font-size:16px;'>{label}</p>"

    st.markdown(s, unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        #st.session_state["messages"] = [{"role":"assistant", "content":"Hi! Provide location to search for tree information?"}]

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "selected_trees" not in st.session_state:
        st.session_state["selected_trees"] = []

    if "ConversionFlag" not in st.session_state:
        st.session_state["ConversionFlag"] = 0

    if "query" not in st.session_state:
        st.session_state["query"] = "" 

    for msg in st.session_state.messages:          
        st.chat_message(msg["role"]).write(msg["content"])
        #with st.chat_message(msg["role"]):
            #st.markdown(msg["content"])
            

    if query := st.chat_input("Hi! Provide location to search for tree information?"):
        response=""
        if (query=="exit"):
            st.session_state["chat_history"]=[]
            st.session_state["ConversionFlag"]=0
            st.session_state["query"] = ""
            st.session_state["selected_trees"] = []
                
            #st.session_state.messages.append({"role": "assistant", "content": "Hi! ?"})
            #for msg in st.session_state.messages:
                #st.chat_message(msg["role"]).write(msg["content"])
                        
            st.session_state["messages"] = []

        else:
            st.session_state["ConversionFlag"] += 1
            st.session_state["query"]=query

        if (st.session_state["ConversionFlag"]==1):
            #invoke get_response_custom_agent
            chat_history = st.session_state["chat_history"]

            sel_trees , response = get_response_custom_agent(query ,chat_history)

            chat_history.extend(
                [
                    HumanMessage(content=query),
                    AIMessage(content=response),
                ]
            )

            #Refresh Map 
            if len(sel_trees) > 0 :          
                df = pd.DataFrame.from_dict(sel_trees)    

            st.session_state["chat_history"] = chat_history
            st.session_state["selected_trees"] = sel_trees 
            print("Response to first conversion:" + str(response))

        elif(st.session_state["ConversionFlag"]>1):

            #invoke RAG

            #Get context from chat history
            chat_history = st.session_state["chat_history"]
            selected_trees = st.session_state["selected_trees"] 

            if len (selected_trees) > 0 :
                response = get_response_retrieverFFW( query ,chat_history , selected_trees)
                #Refresh Map 
                df = pd.DataFrame.from_dict(selected_trees)        
            else:
                response = "Please type exit and try searching for trees in a new location"
            
            print("Response to continue conversion:" + str(response))
            chat_history.extend(
                [
                    HumanMessage(content=query),
                    AIMessage(content=response),
                ]
            )          
            st.session_state["chat_history"] = chat_history
            
        if (st.session_state["ConversionFlag"] >= 1):

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(query)            
            with st.chat_message("assistant"):
                st.markdown(response)   
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
                

            #st.chat_message("user").write(query)
            #msg = str(response)
            #st.chat_message("assistant").write(msg)


    #display map
    #with row1_col1:
        
    # plot all treessg
    fig = px.scatter_mapbox(df , lat="lat",lon="lng",hover_name="tree_id",hover_data=["height_est","age"],
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
 

    with st.expander("Disclaimer"):
        st.write(
                """

                IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

                Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

                Always consult with qualified professionals for accurate and personalized advice.

                """
        )
        
    
if __name__ == "__main__":
    # Check if the password is correct.  
    if not check_password():
        st.stop()
    main()