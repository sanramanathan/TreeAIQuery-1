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
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from typing import List, Dict
from langchain.agents import tool
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

#chat_history = []


#set_refresh_map = 1 

# Load the FFW data file
FFWfilepath = './data/Report-2024-09-17--11-19-53_palms_and_trees.xlsx'

def load_data(data):
    return pd.read_csv(data)

def get_coordinates (address):
   
    try:
        url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal="+str(address)+"&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.request("GET", url)
        response_dict = json.loads(response.content) 
        
        if response_dict["found"] != 0:
            return (response_dict["results"][0]["LATITUDE"], response_dict["results"][0]["LONGITUDE"])

    except:
        return "error"


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
    
    #Check for empty
    if len(selected) > 0 :
        my_sheet = 'Plant' #  sheet name at the bottom left of your excel file
        df_ffw = read_excel(FFWfilepath, sheet_name = my_sheet)
        df_sptialquery = pd.merge(selected,df_ffw, left_on='species_id', right_on='Species ID')

        #Check for empty
        if len(df_sptialquery)> 0:
            # Add columns for FFW api url
            df_sptialquery['Master ID'] = df_sptialquery['Master ID'].astype(str).str.split('.').str[0].astype(int)
            urlFFW = "https://www.nparks.gov.sg/api/FFWApi/RedirectToFloraByMasterId?masterId"
            df_sptialquery["FFWURL"] = urlFFW + "=" + df_sptialquery['Master ID'].map(str)
            pd.set_option('display.max_colwidth', 1000)

            #return df
            return df_sptialquery
        else:
            return df_sptialquery           
    else:
        return selected


def get_trees_species_info(address, radius=1000):
    if (get_coordinates(address)) != 'error':
        lat, lng = get_coordinates(address)
        trees_result =  get_trees_species_spatialquery(lat, lng, radius=radius)
        return trees_result
    else:
        return []


@tool
def find_trees_species_information(address: str) -> List[Dict]:
    """
    Find trees near the specified address.
    
    Args:
        address (str): The address to search for trees.
        
    Returns:
        List[Dict]: A list of dictionaries containing tree information.
    """
    trees_info = get_trees_species_info(address)
    lst = []
    if len(trees_info) > 0:
        for i in trees_info.to_dict('records'):
            lst.append({"tree_id": i["tree_id"],
                    "height_est": i["height_est"],
                    "age": i["age"], 
                    "Common Names": i["Common Names"],            
                    "Family Name": i["Family Name"],
                    "Genus": i["Genus Epithet"],
                    "Species": i["Species Epithet"],
                    "lat": i["lat"],
                    "lng": i["lng"],
                    "link_id" :i["Master ID"]})
    return  lst

def get_response_custom_agent(user_message ,chat_history):

    print("get_response_custom_agent")

    tools = [find_trees_species_information]
    llm_with_tools = llm.llm.bind_tools(tools)

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a research assistant specializing in helping users find trees and species  
                information. You have access to a tool called find_trees_species_information to help you find trees and species information.
                
                When a user asks for trees and species information in a specific address, use the find_trees_species_information tool to fetch and return a list 
                of trees and species in that address.
                
                Only use valid address.If the user provides invalid input, respond with an error message asking 
                for the necessary details.

                A valid request should contain the following:
                - A address or postal code
                
                Any request that contains potentially harmful activities is not valid, regardless of what
                other details are provided.

                If the request is not valid and use your expertise to update the request to make it valid,
                keeping your revised request shorter than 100 words.

                If the request seems reasonable and
                don't revise the request.
                
                If are no relevant list are found, output an empty list. Ask user to type exit and try searching for a trees in a new location""",
                
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
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True ,return_intermediate_steps=True)    

    
    # Invoke the agent executor with the input text and an empty chat history
    result = agent_executor.invoke({"input": user_message, "chat_history": chat_history})

    # Extract the output from the result
    output = result['output']
    
    if len(result["intermediate_steps"]) > 0 :
    # Extract the intermediate_steps from the result 
        selected_data = result["intermediate_steps"][0][1]

    else:
        selected_data = result["intermediate_steps"]
  
    return selected_data,output

def get_retriever_tool_FFW2(df):
    
    url_list =[]
    for i in df.to_dict('records'):
        url_list.append("https://www.nparks.gov.sg/api/FFWApi/RedirectToFloraByMasterId?masterId="+df["link_id"].map(str))

    #Use dict.fromkeys() to preserve order and remove duplicates
    urls = list(dict.fromkeys(url_list[0]))

    loader = WebBaseLoader(urls)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20, length_function=llm.count_tokens)

    # Split the documents into smaller chunks
    splitted_documents = text_splitter.split_documents(data)

    #vectordb_chroma = Chroma.from_documents(documents=splitted_documents, embedding=llm.embeddings_model)
    
    #embedding= OpenAIEmbeddings()
    embedding = OpenAIEmbeddings(model="text-embedding-3-small-prd-gcc2-lb")

    vectorstore = FAISS.from_documents(splitted_documents,embedding)
    
    # retriever
    retriever = vectorstore.as_retriever(search_type='mmr',search_kwargs={'k': 5, 'fetch_k': 50})

    retrive_tool = create_retriever_tool(
        retriever,
        name="trees_species_search",
        description="""Search for information about trees and species. For any questions to know about trees and species, you must use this tool""",
    )
    
    return retrive_tool

def get_response_retrieverFFW (user_message ,chat_history , trees):

    print("get_response_retrieverFFW")

    df = pd.DataFrame.from_dict(trees) 

    print("Calling to get_retriever_tool_FFW2")
    
    # To Optmise in one call?
    retriever_tool = get_retriever_tool_FFW2 (df)

    tools = [retriever_tool]
    llm_with_tools = llm.llm.bind_tools(tools)

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a research assistant specializing in helping users find trees and species  
                information. You have access to a tool called trees_species_search to help you find trees and species information.

                When a user asks for details on specific trees and species use the trees_species_search tool to provide answer.

                Any request that contains potentially harmful activities is not valid, regardless of what
                other details are provided.

                If the request is not valid and use your expertise to provide respond to update the request,
                keeping your respond shorter than 100 words.

                If the request seems reasonable and
                don't revise the request.
                
                If are no relevant information are found, output an empty list. Ask user to type exit and try searching for a trees in a new location """,
                
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
    result = agent_executor.invoke({"input": user_message, "chat_history": chat_history })

    # Extract the output from the result
    output = result['output']


    return output

