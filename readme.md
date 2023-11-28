# WebChat Explorer

WebChat Explorer is a versatile tool that combines web scraping with interactive chat capabilities, providing users with a seamless experience to explore and interact with information from any website.

## Overview

<div align="center"><img src="docs/WebChatExplorer.gif" width="800"></div>

&nbsp;

This project has two main functionalities:

### 1. Web Scraper:

* Users can scrape information from any website by providing the desired domain.
* The HTML of the webpage is retrieved using the `requests` library.
* `bs4` (Beautiful Soup) parses the HTML code, extracting text and links.
* The parsed information is presented to the user, with options to download the extracted text or links.

### 2. Interactive Chat with Text Similarity Search:

* Users can upload a file and engage in an interactive chat with the system.
* Text similarity search is performed using `scikit-learn` to find relevant text chunks based on user queries.
* The chatbot leverages OpenAI's GPT-3.5 (Chat GPT) language model to generate responses to user queries.
* The chat history is maintained in the `st.session_state` dictionary, persisting across Streamlit sessions.

## Dependencies

This project relies on the following libraries:
- `streamlit`: for building the user interface.
- `openai`: for generating responses to user questions.
- `tiktoken`: for tokenizing text
- `scikit-learn`: for finding the relevant text chunks based on a user's question.
- `numpy`: for creating arrays
- `pandas`: for creating dataframes
- `bs4`: for parsing HTML code.
- `requests`: for retreiving the HTML of a webpage.

## Usage

Follow these steps to set up and run the project:

1. Create a virtual environment:
```
python3 -m venv my_env
source my_env/bin/activate # Mac OS or Linux
.\my_env\Scripts\activate # Windows
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the Streamlit server:
```
streamlit run main.py
streamlit run app.py
```

Access the web scraper by navigating to `http://localhost:8501` and the conversational chatbot by visiting `http://localhost:8502`. 

## How it Works

### Web Scraper:
1. User enters a URL in the input field.
2. `requests` retrieves relevant HTML based on the user's URL.
3. `bs4` parses the HTML code into text and links.
4. The chatbot displays parsed information, providing options to download text or links.

### Interactive Chat:
1. User enters a question in the input field.
2. Text similarity search using `scikit-learn` retrieves relevant text chunks.
3. User's question is added to retrieved text chunks to create an augmented query.
4. GPT-3.5 generates a response to the augmented query.
5. The chatbot displays the response, along with the chat history.

The chat history is stored in the `st.session_state` dictionary for persistence.