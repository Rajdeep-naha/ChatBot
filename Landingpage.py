import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
from model import model

history = list()

load_dotenv()
hf_api_key = os.getenv("HUGGING_FACE_API")
client = InferenceClient(api_key=hf_api_key)

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.sidebar.header("SIDEBAR")

col1, col2 = st.columns([0.75, 8])

with col1:
    st.image(Image.open("image.png"), width=100)

with col2:
    st.title('CHATBOT V1.0')

st.write('### CHAT AWAY')


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  

x = "Hello! I am a chatbot. I can answer your questions. Ask me anything."

if prompt := st.chat_input('Ask anything'):

    with  st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Generating"):
        x = model(prompt,client,hf_api_key,history)


with  st.chat_message('assistant'):
    st.markdown(x)
st.session_state.messages.append({"role": "assistant", "content": x})



