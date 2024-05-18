import os
import re
import streamlit as st

from elasticsearch import Elasticsearch
from openai import OpenAI
from streamlit_chat import message

os.environ["RABBITMQ_HOST"] = "localhost"

CHUNK_SIZE = 400
ES_CHUNK_SIZE = 50
INDEX_NAME = "es_french_revo_idx"
MODEL_ID = "BAAI/bge-large-zh-v1.5"
MODEL_ID_ES = "baai__bge-large-zh-v1.5"
MODEL_DIM = 1024
MODEL_SIMILARITY = "cosine"

ES_HOST = "https://localhost:9200/"
ES_PASS = "y5AADXZR0l63CvTz1AsWznNiAM1Ukq7KSd3MEra"

client = OpenAI(
    api_key="",
)

# Create the client instance
es_client = Elasticsearch(
    # For local development
    hosts=[ES_HOST],
    basic_auth=("elastic", ES_PASS),
    verify_certs=False,
)
print(es_client.info())

st.title("法国大革命历史问答机器人")


def rag_get(question):
    response = es_client.search(
        index=INDEX_NAME,
        knn={
            "inner_hits": {"size": 1, "_source": False, "fields": ["passages.text"]},
            "field": "passages.vector.predicted_value",
            "k": 20,
            "num_candidates": 100,
            "query_vector_builder": {
                "text_embedding": {
                    "model_id": MODEL_ID_ES,
                    "model_text": question,
                }
            },
        },
    )
    return [hit["_source"]["text"] for hit in response["hits"]["hits"]]


def api_calling(prompt):
    completions = client.chat.completions.create(  # Change the method
        model="gpt-4",
        messages=msg,
        stream=True,
    )
    return completions


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    rag_responses = rag_get(prompt)
    msg = [  # Change the prompt parameter to messages parameter
        {"role": "assistant", "content": rag_response} for rag_response in rag_responses
    ]
    msg += [{"role": "user", "content": prompt}]
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=msg,
            stream=True,
        )
        response = st.write_stream(stream)
