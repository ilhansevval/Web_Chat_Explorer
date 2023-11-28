import numpy as np
import streamlit as st
import tiktoken as tk
import docx2txt
import openai
from about import about
from sklearn.metrics.pairwise import cosine_similarity

from api_key import openai_api_key
openai.api_key = openai_api_key

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

@st.cache_resource
def tokenize(text):
    enc = tk.encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    return tokens
  
@st.cache_resource
def chunk_tokens(tokens, chunk_length=40, chunk_overlap=10):
    chunks = []
    for i in range(0, len(tokens), chunk_length - chunk_overlap):
        chunks.append(tokens[i:i + chunk_length])
    return chunks

@st.cache_resource
def detokenize(tokens):
    enc = tk.encoding_for_model("gpt-4")
    text = enc.decode(tokens)
    return text

@st.cache_resource
def embed_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embeddings.append(get_embedding(chunk))
    return embeddings
with st.sidebar:
    about()

    st.write('  ') 
    st.markdown("""---""")
    if not openai_api_key:
        openai_api_key = st.text_input("# OpenAI API Key", key="chatbot_api_key", type="password")
        col1, col2 = st.columns([1,5], gap="medium")
        with col2:
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    upload = st.file_uploader("Upload a document")

if not upload: 
    st.text('''Upload a document to get started''')
with st.sidebar:
    if upload:
        if upload.name.endswith(".txt"):
            document = upload.read().decode("utf-8")
        if upload.name.endswith(".docx") or upload.name.endswith(".doc") or upload.name.endswith(".pdf") or upload.name.endswith(".png") or upload.name.endswith(".jpg"):
            with st.spinner('Extracting Text...'):
                document = docx2txt.process(upload)
                document = document.replace("\n", " ")
                document = document.replace("  ", " ")
                document = document.encode('ascii', 'ignore').decode()
                document = document.replace("&", "and")

        st.write('  ') 
        st.subheader('Document Embeddings')

        tokens = tokenize(document)
  
        n_tokens = np.array(tokens).size
        st.write("tokens: ", n_tokens)

        token_chunks = chunk_tokens(tokens)
        n_token_chunks = len(token_chunks)

        word_chunks = [detokenize(chunk) for chunk in token_chunks]
        n_word_chunks = len(word_chunks)
  
        st.write("word chunks: ", n_word_chunks)
        doc_embeddings = embed_chunks(word_chunks)
        st.write("embeddings: ", np.array(doc_embeddings).shape)

        st.write('  ') 
        st.sidebar.subheader('Document')
        st.sidebar.write(document)

if upload:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Write a message"):
        st.chat_message("user").write(prompt)
        prompt_embedding = get_embedding(prompt)
        similarities = []
        for doc_embedding in doc_embeddings:
            similarities.append(cosine_similarity([prompt_embedding], [doc_embedding])[0][0])
        n = 2
        idx_top_n_scores = np.argsort(similarities)[-n:][::-1]
        context = ""
        for idx in idx_top_n_scores:
            context += word_chunks[idx] + " "
        final_prompt = """Answer the question or statement using the 
        context provided, you need to be clear and concise, sometime funny.
        If you need to make an assumption you must say so. 
        The question or statement you must answer is: """ + prompt + "." + """ remember to be concise and clear.
        
        Use this context: """ + context
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        response = openai.ChatCompletion.create(model="gpt-4", messages=st.session_state.messages)
        st.session_state.messages.pop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)
        with st.expander("Context"):
            st.write(context)