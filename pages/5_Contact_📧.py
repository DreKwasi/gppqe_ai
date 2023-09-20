import streamlit as st
from helper_func import styles, utils
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

st.set_page_config(
    page_title="PharmAssist",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.local_css("styles/main.css")
# styles.local_css("styles/contact_form.css")

st.subheader("📥 Your feedback is king !")
col1, col2 = st.columns([2, 1])
# contact_form = """
# <form action="https://formsubmit.co/f019594dc785ee264df1d144b7593265 " method="POST">
#     <input type="hidden" name="_captcha" value="true">
#     <input type="text" name="name" placeholder="Your name" required>
#     <input type="email" name="email" placeholder="Your email" required>
#     <textarea name="message" placeholder="Your message here"></textarea>
#     <button type="submit">Send</button>
# </form>
# """
# contact_form = """<a href="https://formsubmit.co/el/kuzosa" target="_blank">Email us</a>"""
# col1.markdown(contact_form, unsafe_allow_html=True)
with col1.form("contact_form", clear_on_submit=False):
    name = st.text_input("name", label_visibility="collapsed", placeholder="Name")
    email = st.text_input("email", label_visibility="collapsed", placeholder="Email")
    comment = st.text_input("feedback", label_visibility="collapsed", placeholder="Feedback")
    submit = st.form_submit_button("Send Feedback", type="primary")


if submit:
    name = name.strip().title()
    email = email.strip()
    if utils.validate_email(email):
        details = {"name": name.title(), "email": email, "created_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "feedback":feedback}
        response = db.update_user(details)
        if response:
            st.success("We have received your feedback. Hope you enjoy the application")
            st.balloons()
        else:
            st.error("You are already registered")
    else:
        st.error("Invalid Email Address")


lottie_comment = utils.load_lottiefile("animations/email_us.json")

with col2:
    st_lottie(
        lottie_comment,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", # medium ; high
        height=400,
        width=None,
        key=None,
    )
