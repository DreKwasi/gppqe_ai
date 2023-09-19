import streamlit as st
from helper_func.llm_model import *
from helper_func.text_utils import clinical_options, subjective_question_prompt, subject_answer_prompt, health_act_options

# Page settings
st.set_page_config(
    page_title="PharmaAssist",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
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

    st.write("Topics")
    sel_topics = st.multiselect(
        "topics",
        default="Disorders_of_the_GIT"
        if sel_dis == "Standard Treatment Guidelines"
        else "Tobacco Control Measures",
        options=clinical_options
        if sel_dis == "Standard Treatment Guidelines"
        else health_act_options,
        placeholder="Select a topic",
        label_visibility="collapsed",
    )
    col1, col2 = st.columns(2)

    user_question = ""
    ai_question = ""
    chat_history = []
    if col1.button("Generate quiz", type="primary"):
        user_question = f"Ask me any random question on {sel_topics}"

        with st.spinner("Generating open-ended question"):
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
st.title("Open Ended Quiz")
st.toast("This is a demo of the PharmaAssist AI. Please use it as a learning tool.")

if col2.button("Reset Chat"):
    del st.session_state["messages"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []


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

    with st.spinner("Generating response..."):
        conversationChain, mermory = get_conversation_chain(
            st.session_state["vectorStore"], subject_answer_prompt, input_key="question"
        )
        mermory.clear()
        answer_history = []

        response = conversationChain(
            {
                "question": st.session_state["ai_question"],
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
