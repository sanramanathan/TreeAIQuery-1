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
with st.expander("Disclaimer"):
    st.write(
            """

            IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

            Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

            Always consult with qualified professionals for accurate and personalized advice.

            """
        )



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

    st.header("Our Solution")
    st.write("""
    TreeQuery AI leverages advanced chatbot technology, generative AI, Retrieval-Augmented Generation (RAG), and geospatial analysis to streamline access, analysis, and visualisation of tree data from the TreesSG and Flora Fauna Web (FFW) databases. This proof-of-concept aims to significantly enhance the efficiency and effectiveness of NParks' research and conservation efforts while reducing time spent on manual data searches.
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

if __name__ == "__main__":
    about_us_page()
