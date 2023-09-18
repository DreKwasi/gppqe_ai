import streamlit as st
from helper_func.llm_model import *
from helper_func.text_utils import *

# Page settings
st.set_page_config(
    page_title="Pharmacy Quiz Master",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="auto",
)

# Sidebar
with st.sidebar:
    st.header("Options")

    st.write("Discipline")
    sel_dis = st.selectbox(
        "quiz_type",
        options=["Standard Treatment Guidelines", "Public Health Act"],
        label_visibility="collapsed",
    )

    clinical_options = ["Diabetes", "Hypertension"]
    health_act_options = ["Communicable Disease", "Vaccination", "Immunization"]
    
    st.write("Topics")
    sel_topics = st.multiselect(
        "topics",
        default="Diabetes" if sel_dis == "Standard Treatment Guidelines" else "Communicable Disease",
        options= clinical_options if sel_dis == "Standard Treatment Guidelines" else health_act_options,
        placeholder="Select a topic",
        label_visibility="collapsed",
    )


def get_embeddings(text_data, document):
    with st.spinner("Loading PDF Files"):
        chunks = get_text_chunks(text_data)
        vectorStoreObj = get_vectorstore(chunks, document)
        st.session_state["vectorStore"] = vectorStoreObj


if "discipline_type" not in st.session_state:
    st.session_state["discipline_type"] = ""

if st.session_state["discipline_type"] != sel_dis:
    if sel_dis == "Standard Treatment Guidelines":
        text_data = get_pdf_text("data/stg.pdf")
        get_embeddings(text_data, document="stg")

    elif sel_dis == "Public Health Act":
        text_data = get_pdf_text("data/public_health_act_2012.pdf")
        get_embeddings(text_data, document="pha")

    st.session_state["discipline_type"] = sel_dis


# Main
st.title("Subjective Quiz")
col1, col2 = st.columns(2)

with col1:
    if st.button("Reset Chat"):
        del st.session_state["messages"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

with col2:
    user_question = ""
    ai_question = ""
    chat_history = []
    if st.button("Generate quiz", type="primary"):
        user_question = f"Ask me any random question on {sel_topics}?"

        with st.spinner("Generating quiz"):
            conversationChain, mermory = get_conversation_chain(
                st.session_state["vectorStore"],
                subjective_question_prompt,
                input_key="question",
            )
            mermory.clear()
            response = conversationChain(
                {"question": user_question, "chat_history": chat_history}
            )

        chat_history.append(response["answer"])
        ai_question = response["answer"]

# Display messages on rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question:
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
    st.session_state["messages"].append(
        {"role": "assistant", "content": response["answer"]}
    )
    st.session_state["ai_question"] = ai_question

if answer := st.chat_input("Answer the questions here..."):
    with st.chat_message("user"):
        st.markdown(answer)
    st.session_state["messages"].append({"role": "user", "content": answer})

    conversationChain, mermory = get_conversation_chain(
        st.session_state["vectorStore"], subject_answer_prompt, input_key="question"
    )
    mermory.clear()
    answer_history = []

    response = conversationChain(
        {
            "question": ai_question,
            "chat_history": answer_history,
            "student_answer": answer,
        }
    )
    answer_history.append(response["answer"])
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
    st.session_state["messages"].append(
        {"role": "assistant", "content": response["answer"]}
    )
