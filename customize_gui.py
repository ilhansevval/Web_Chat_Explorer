import streamlit as st

class gui():
    def __init__(self):
        pass
    def about(self, photo = "docs/me.png", author = "Şevval", text = "Here you can ... "):
        with st.sidebar:
            col1, col2, = st.columns([1,2], gap="medium")
            with col1:
                st.image(photo, width=75)
            with col2:
                st.write(f""" 
                Hey it's {author}, \n
                {text}
                """)
            col1, col2, col3, col4, col5, col6 = st.columns([1.1,1,1,1,1,1.5], gap="medium")
            with col2: 
                # Medium
                medium_html = """
                <a href="https://medium.com/@ilhnsevval" target="_blank">
                    <img src="https://www.svgrepo.com/show/445881/medium.svg" alt="Medium Logo" style="width:20px;">
                </a>
                """
                st.write(medium_html, unsafe_allow_html=True)    
            with col3: 
                # Github
                github_html = """
                <a href="https://github.com/ilhansevval" target="_blank">
                    <img src="https://www.svgrepo.com/show/506497/github.svg" alt="Medium Logo" style="width:25px;">
                </a>
                """
                st.write(github_html, unsafe_allow_html=True)
            with col4: 
                # Linkedin
                linkedin_html = """
                <a href="https://www.linkedin.com/in/ilhansevval/" target="_blank">
                    <img src="https://www.svgrepo.com/show/506517/linkedin.svg" alt="Medium Logo" style="width:25px;">
                </a>
                """
                st.write(linkedin_html, unsafe_allow_html=True)

    def clean_format(self):
        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)

    def display_existing_messages(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])