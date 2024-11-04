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
    We utilize state-of-the-art LLM to process user queries. The models are 
    fine-tuned for Singapore-specific tree and geographical data, enhancing their accuracy and reliability. 
    Retrieval-Augmented Generation (RAG) is employed to further improve model performance.
    """)

    st.header("Geospatial Processing")
    st.write("""
    Efficient prompts for spatial queries and calculations are implemented to optimize response times, 
    even with large datasets. The chatbot can handle a wide range of user queries in natural language 
    and display results on an interactive map interface. This includes techniques such as reverse geocoding, 
    buffer and overlay spatial analysis.
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
    st.image(".\data\generic.png", caption="Overview Flowchart")

    st.write("""
    The application has two main use cases:
    1. Chat with information
    2. Intelligent search

    Each use case is illustrated with its own flowchart to depict the process flow.
    """)

    st.subheader("Chat with Information Flowchart")
    st.write("""
    This flowchart illustrates the process of:
    1. Users inputting queries
    2. The LLM processing the queries
    3. The chatbot providing detailed tree information
    """)
    # Placeholder for Chat with Information flowchart
    st.image(".\data\case1.png", caption="Chat with Information Flowchart")

    st.subheader("Intelligent Search Flowchart")
    st.write("""
    This flowchart illustrates the process of:
    1. Users querying an area
    2. The LLM processing the spatial data
    3. The chatbot displaying area-based tree statistics on an interactive map
    """)
    # Placeholder for Intelligent Search flowchart
    st.image(".\data\case2.png", caption="Intelligent Search Flowchart")

    st.write("""
    By implementing these methodologies, TreeQuery AI aims to enhance the efficiency and effectiveness 
    of urban forest management, contributing to better conservation and research efforts in Singapore.
    """)

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
