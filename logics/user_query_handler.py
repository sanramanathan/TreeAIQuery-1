import os
import json
import openai
from helper_functions import llm
import requests
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_excel


from typing import List, Dict
from langchain.agents import tool
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor


# Load the FFW data file
FFWfilepath = './data/Report-2024-09-17--11-19-53_palms_and_trees.xlsx'

def load_data(data):
    return pd.read_csv(data)

def get_coordinates (address):
   
    url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal="+str(address)+"&returnGeom=Y&getAddrDetails=Y&pageNum=1"
    response = requests.request("GET", url)
    response_dict = json.loads(response.content) 

   
    if not response_dict:
        raise ValueError(f"Location for '{address}' not found.")
    
    if response_dict["found"] == 0:
        raise ValueError(f"Location for '{address}' not found.")
    
    if response_dict["found"] != 0:
        return (response_dict["results"][0]["LATITUDE"], response_dict["results"][0]["LONGITUDE"])


def get_trees_species_spatialquery(lat, lng, radius):

    # point in geographic coordinates
    p1 = Point(lng,lat)
    df = pd.DataFrame({'a': [11]})
    p1_gdf = gpd.GeoDataFrame(df,crs=4326, geometry = [p1])

    #Reproject point to metres
    p1_proj = p1_gdf.to_crs(epsg=3414)


    # buffer in meters
    buffer_geometry = p1_proj.buffer(radius, resolution=5, cap_style=1, join_style=1, mitre_limit=2)
    p1_proj['geometry'] = buffer_geometry

    # Load treessg data
    treessg =  load_data("https://raw.githubusercontent.com/sanramanathan/dataAIBootCAMP/refs/heads/main/trees_1000000.csv")
    # CSV into Geomentry
    geometrytrs = [Point(xy) for xy in zip(treessg['lng'], treessg['lat'])]
    crs = {'init' :'epsg:4326'}
    trees = gpd.GeoDataFrame(treessg, crs=4326, geometry=geometrytrs)

    #Reproject trees to metres
    trees_prj = trees.to_crs('EPSG:3414')

    # spatial join to select all trees  within the  buffer region.
    selected = gpd.sjoin(trees_prj, p1_proj, how='inner', predicate='within')

    #selected["FFW"] = urlFFW
    # Correction species_id and SpeciesURL 
    #selected['species_id'] = selected['species_id'].astype(str).str.split('.').str[0].astype(int)

    #selected["SpeciesURL"] = selected['FFW'].map(str) + "=" + selected['species_id'].map(str)
    #pd.set_option('display.max_colwidth', 1000)

    #Now do a  join  selected  trees  within the  buffer region with FFW data
     # Load ffw data
    #FFWdata = "Report-2024-09-17--11-19-53_palms_and_trees.xlsx"
    my_sheet = 'Plant' #  sheet name at the bottom left of your excel file
    df_ffw = read_excel(FFWfilepath, sheet_name = my_sheet)

    df_sptialquery = pd.merge(selected,df_ffw, left_on='species_id', right_on='Species ID')

    # Add columns for FFW api url
    df_sptialquery['Master ID'] = df_sptialquery['Master ID'].astype(str).str.split('.').str[0].astype(int)
    urlFFW = "https://www.nparks.gov.sg/api/FFWApi/RedirectToFloraByMasterId?masterId"
    df_sptialquery["FFWURL"] = urlFFW + "=" + df_sptialquery['Master ID'].map(str)
    pd.set_option('display.max_colwidth', 1000)

    #return df
    return df_sptialquery


def get_trees_species_info(address, radius=1000):
    lat, lng = get_coordinates(address)
    trees_result =  get_trees_species_spatialquery(lat, lng, radius=radius)

    return trees_result


@tool
def find_trees_species_informataion(address: str) -> List[Dict]:
    """
    Find trees near the specified address.
    
    Args:
        address (str): The address to search for trees.
        
    Returns:
        List[Dict]: A list of dictionaries containing tree information.
    """
    trees_info = get_trees_species_info(address)

    lst = []
    for i in trees_info.to_dict('records'):
        lst.append({"tree_id": i["tree_id"],
                "height_est": i["height_est"],
                "age": i["age"], 
                "Common Names": i["Common Names"],            
                "Family Name": i["Family Name"],
                "Genus": i["Genus Epithet"],
                "Species": i["Species Epithet"],
                "latitude": i["lat"],
                "Longitude": i["lng"]})
    return  lst


def generate_response (user_message):
    tools = [find_trees_species_informataion]
    llm_with_tools = llm.llm.bind_tools(tools)

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a research assistant specializing in helping users find trees and species  
                informatation. You have access to a tool called find_trees_species_informataion to help you find trees and species informatation.
                
                When a user asks for trees and species informatation in a specific postalcode, use the find_trees_species_informataion tool to fetch and return a list 
                of trees and species in that postalcode.
                
                Only use valid address.If the user provides invalid input, respond with an error message asking 
                for the necessary details.

                A valid request should contain the following:
                - A postalcode 
                
                Any request that contains potentially harmful activities is not valid, regardless of what
                other details are provided.

                If the request is not valid and use your expertise to update the request to make it valid,
                keeping your revised request shorter than 100 words.

                If the request seems reasonable and
                don't revise the request.""",
                
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)    

    

    # Invoke the agent executor with the input text and an empty chat history
    result = agent_executor.invoke({"input": user_message, "chat_history": []})

    # Extract the output from the result
    output = result['output']

    return output


def process_user_message(user_input):

    # Process 1: Get the Trees Details
    trees_infos = get_trees_species_info(user_input)

    # Process 2: Generate Response based on Course Details
    reply = generate_response(user_input)

    return reply ,trees_infos



