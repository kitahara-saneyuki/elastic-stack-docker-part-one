import streamlit as st
from openai import OpenAI
from streamlit_chat import message

st.title("ChatGPT ChatBot With Streamlit and OpenAI")

client = OpenAI(
    api_key="",
)

def api_calling(prompt):
    completions = client.chat.completions.create(  # Change the method
        model="gpt-4",
        messages=[  # Change the prompt parameter to messages parameter
            {"role": "user", "content": prompt},
        ],
    )
    message = completions.choices[0].message.content
    return message


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
    output = output.lstrip("\n")

    # Store the output
    st.session_state.openai_response.append(user_input)
    st.session_state.user_input.append(output)

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
