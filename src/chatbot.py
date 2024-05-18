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
st.title("ChatGPT ChatBot With Streamlit and OpenAI")


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
    rag_responses = rag_get(prompt)
    print(rag_responses)
    msg = [  # Change the prompt parameter to messages parameter
        {"role": "assistant", "content": rag_response} for rag_response in rag_responses
    ]
    msg += [{"role": "user", "content": prompt}]
    completions = client.chat.completions.create(  # Change the method
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    return completions


if "user_input" not in st.session_state:
    st.session_state["user_input"] = []

if "openai_response" not in st.session_state:
    st.session_state["openai_response"] = []


def get_text():
    input_text = st.text_input("write here", key="input")
    return input_text


user_input = get_text()

if user_input:
    output = api_calling(user_input)

    # Store the output
    st.session_state.openai_response.append(user_input)
    response = st.write_stream(output)
    st.session_state.user_input.append(response)

message_history = st.empty()

if st.session_state["user_input"]:
    for i in range(len(st.session_state["user_input"]) - 1, -1, -1):
        # This function displays user input
        message(st.session_state["user_input"][i], key=str(i), avatar_style="icons")
        # This function displays OpenAI response
        message(
            st.session_state["openai_response"][i],
            avatar_style="miniavs",
            is_user=True,
            key=str(i) + "data_by_user",
        )
