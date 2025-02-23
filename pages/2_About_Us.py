import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="TreeAI Query Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->


def about_us_page():
    st.title("About Us")

    st.header("Welcome to TreeQuery AI")
    st.write("TreeQuery AI is an innovative project by NParks, the organisation managing Singapore's extensive urban forest. Our mission is to revolutionise urban forest management through intelligent data access and analysis.")

    st.header("The Challenge")
    st.write("""
    NParks manages data on hundreds of trees stored in the TreesSG database. Researchers, staff, and the public frequently need to access and analyse this data for various purposes, including tree care, conservation planning, and environmental monitoring. However, the current data retrieval process is inefficient and time-consuming, often requiring multiple database queries and manual cross-referencing.
    
    This inefficiency impacts NParks' operations by:
    - Diverting researchers and staff from critical analysis and fieldwork
    - Delaying responses to public inquiries
    - Limiting the depth and breadth of research due to time constraints
    - Risking oversight of important trends or issues
    - Hindering new or less experienced staff in accessing and interpreting data effectively
    """)
    st.write("How can we develop an AI-powered system to streamline access, analysis, and visualisation of tree data from the TreesSG database, thereby enhancing the efficiency and effectiveness of NParks' research and conservation efforts while reducing time and resources spent on manually searching for data for analysis?")


    st.header("Our Solution")
    st.write("""
    TreeQuery AI leverages advanced chatbot technology, generative AI, Retrieval-Augmented Generation (RAG), and geospatial analysis to streamline access, analysis, and visualisation of tree data from the TreesSG and Flora Fauna Web (FFW) databases. This proof-of-concept aims to significantly enhance the efficiency and effectiveness of NParks' research and conservation efforts while reducing time spent on manual data searches.
    """)

    st.subheader("Project Scope")
    st.write("""
    - It aims to create a user-friendly interface that can process natural language queries, retrieve comprehensive tree data, and display results on an interactive map through the integration of advanced technologies including generative AI, Retrieval-Augmented Generation (RAG), and geospatial analysis.
    - The scope includes developing capabilities for both NParks staff and public users, covering aspects such as tree identification, location mapping, and data analysis for research and conservation purposes.
    """)

    st.header("Objectives")
    st.write("""
    1. Develop a chatbot that can accurately interpret and respond to natural language queries about trees
    2. Create an efficient system for retrieving and visualising tree data from existing databases
    3. Reduce the time and resources spent on manual data searches by NParks staff
    4. Enhance the capacity for data-driven research and decision-making in urban forest management
    5. Improve public access to information about local trees and green spaces
    6. Support Singapore's vision as a City in Nature by fostering greater appreciation and understanding of the urban forest
    """)
    

    st.subheader("Data sources")
    st.write("""
    - TreesSG database ( csv file)
    - Fauna and Flora database (excel file)
    """)

    st.subheader("Key Features")
    st.write("""
    - Natural language processing for intuitive data queries
    - Comprehensive tree information retrieval (scientific names, age, planting date, dimensions, coordinates)
    - Interactive map interface for visualising tree locations
    - Efficient data analysis capabilities
    """)

    st.write("""
    By addressing the challenges in data accessibility and analysis, TreeQuery AI empowers NParks to make more informed decisions, respond quickly to inquiries, and dedicate more resources to critical conservation and research efforts. By extension, TreeQuery AI also aims to provide an interactive and informative experience for users, fostering greater interest in flora and fauna in our gardens.
    """)


    st.header("Impact")
    st.write("""
    The implementation of TreeQuery AI aims to enhance NParks' operations and research capabilities. By providing streamlined access to tree data through natural language queries, the system is designed to improve the efficiency of researchers and staff. It has the potential to facilitate ecological studies, field work preparation, and long-term monitoring of trees in Singapore. This tool is expected to support more data-driven research and collaboration across teams, which could contribute to improved management and conservation of Singapore's urban forest.

    TreeQuery AI also has the potential to positively impact public engagement with Singapore's urban greenery. By offering location-specific tree information, it may enhance public awareness and appreciation of the urban forest. In urban planning and tree management, the system could provide useful insights for species selection and maintenance planning, potentially improving the efficiency of tree care and urban greening efforts.

    Looking ahead, TreeQuery AI might be developed to support educational initiatives through interactive, location-based learning activities. By potentially reducing response times to tree-related concerns, it could play a role in maintaining the health of Singapore's urban forest, which provides valuable ecosystem services. This innovative system aligns with Singapore's vision of being a City in Nature and may help foster a stronger connection between citizens and their green surroundings.
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
    about_us_page()
