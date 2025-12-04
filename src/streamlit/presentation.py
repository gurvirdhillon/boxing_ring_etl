import streamlit as st

st.title("Welcome to the ETL Boxing Project")

st.subheader("Goals of the project")

st.markdown("""
1) Extract the data from its sources.  
    1.1) Use web scraping to generate images of boxers upon request.
2) Produce a clean dataset of boxing data.
3) Create an automated engineering pipeline.
4) Build an analytics platform.
5) Use testing to identify key areas of development.
""")

st.subheader("Miro Diagram for the boxing ETL project Explained:")

miro_url = "https://miro.com/app/live-embed/uXjVJh8xNIY=/?embedMode=view_only_without_ui&moveToViewport=-3643%2C-2071%2C6599%2C4931&embedId=252787849467"
st.components.v1.iframe(miro_url, width=1200, height=800)
