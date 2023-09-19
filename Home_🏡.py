import streamlit as st
from streamlit_extras.switch_page_button import switch_page


# Page title and description
st.title("Pharmacist Licensure Exam Prep 👨🏽‍⚕️👩🏽‍⚕️")
st.write("Welcome to the Pharmacist Licensure Exam Prep App. This app is designed to help pharmacists prepare for their licensure exam by providing multiple choice questions based on the Ghanaian Standard Treatment Guidelines and the Public Health Act. Additionally, we offer a chatbot for assessing open-ended questions.")

# Navigation options
col1, col2 = st.columns(2)
if col1.button("Get started with open ended quiz assessment", type="primary", use_container_width=True):
        switch_page("Open_Ended_Quiz")
if col2.button("Get started with multiple choice questions", type="primary", use_container_width=True):
        switch_page("Multiple_Choice")

    
# Features to come (Leaderboard, Newsletter, Flashcards)
st.write("### Upcoming Features")
st.write("Stay tuned for these exciting features coming soon:")
st.write("- Leaderboard: Compete with others and track your progress.")
st.write("- Newsletter: Subscribe to our newsletter for the latest updates and tips.")
st.write("- Flashcards: Study key topics with interactive flashcards.")

# Footer or contact information
st.write("For any inquiries or support, please contact me at andrewsboateng137@gmail.com")
