import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Methodology"
)
# endregion <--------- Streamlit App Configuration --------->

import streamlit as st

def methodology_page():
    st.title("Methodology")

    st.write("""
    The methodology behind TreeQuery AI involves a comprehensive approach to data flows and implementation. 
    Our system combines data integration, Large Language Model (LLM) technology, and geospatial processing 
    to deliver accurate and reliable information to users.
    """)

    st.header("Data Integration")
    st.write("""
    We combine the NParks TreesSG database with tree species data from the Flora and Fauna Website (FFW). This integration supports the LLM in processing 
    user queries and providing detailed tree information.
    """)

    st.header("LLM Integration")
    st.write("""
    We utilize state-of-the-art LLMs i.e GPT-4o mini to process user queries. The models are 
    fine-tuned for Singapore-specific tree and geographical data, enhancing their accuracy and reliability. 
    Retrieval-Augmented Generation (RAG) is employed to further improve model performance.
    """)

    st.header("Geospatial Processing")
    st.write("""
    Efficient prompts for spatial queries and geospatial toolkit (OneMap API reverse geocoding, 
    buffer analysis, spatial join and attribute join) are implemented to optimize response 
    times, even with large datasets. The chatbot can handle user queries in natural language 
    and display results on an interactive map interface.
    """)

    st.header("User Interface")
    st.write("""
    A user-friendly chat interface is developed, integrating an interactive map for visual representation 
    of results. This interface allows users to easily access and navigate tree information.
    """)

    st.header("Tech stack")
    st.write("""
    - LLM Model GPT-4o-mini
    - GeoPandas library for spatial anlaysis
    - OpenAI embedding model (text-embedding-3-small) 
    - Facebook AI Similarity Search (Faiss) Vector library 
    """)

    st.header("Flowcharts")

    # Placeholder for Chat with Information flowchart
    st.image("./data/generic.png", caption="Generic flowchart")

    st.write("""
    The application has two main use cases:
    1. User searches for trees and tree information via postal code or address
    2. After query 1, user asks for more information on a particular tree species

    Each use case is illustrated with its own flowchart to depict the process flow. Users can type "exit" 
    to start a new query or continue with the existing conversation.
    """)


    st.subheader("Use Case 1: Tree Search by Location")
    st.write("""
    This flowchart illustrates the process of:
    1. User inputs a query for trees in a specific area using postal code or address.
    2. The Large Language Model (LLM) processes the query to understand the intent and extract relevant information.
    3. The LLM activates a geospatial processing toolkit to search the TreesSG database for matching trees.
    4. The system retrieves corresponding information from the Flora Fauna Web (FFW) database.
    5. The application displays results by plotting tree locations on an interactive map and generating a text response.
    """)
    # Placeholder for Tree Search by Location flowchart
    st.image("./data/case1.png", caption="Tree Search by Location Flowchart")

    st.subheader("Use Case 2: Detailed Tree Species Information")
    st.write("""
    This flowchart illustrates the process of:
    1. User requests more information on a particular tree species identified in Use Case 1.
    2. The system constructs a web URL for the specific tree species on the FFW website.
    3. Using Retrieval-Augmented Generation (RAG):
       a) The system accesses pre-loaded and embedded webpages from the FFW site, stored in a vector database.
       b) The LLM uses the query to search the vector database for relevant information.
       c) The system applies Maximum Marginal Relevance (MMR) to retrieve or summarize pertinent information.
    4. The chatbot presents the retrieved or summarized information to the user.
    """)
    # Placeholder for Detailed Tree Species Information flowchart
    st.image("./data/case2.png", caption="Detailed Tree Species Information Flowchart")

    with st.expander("Disclaimer"):
        st.write(
                """

                IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

                Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

                Always consult with qualified professionals for accurate and personalized advice.

                """
            )
if __name__ == "__main__":
    methodology_page()
