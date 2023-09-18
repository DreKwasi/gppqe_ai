# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from streamlit_extras.metric_cards import style_metric_cards

# st.set_page_config(page_title="GPPQE", page_icon=":house:", layout="centered")

# # Set the title and introduction
# st.title("Ghanaian Treatment Guidelines Quiz Generator")
# st.write("Welcome to our quiz generator based on the Ghanaian Standard Treatment Guidelines.")

# # App Heading
# st.header("Quiz Scores and Leaderboard")

# # from firebase_admin import credentials, firestore, initialize_app

# # Initialize Firebase (replace with your service account key)
# # cred = credentials.Certificate("your-service-account-key.json")  # Replace with your service account key
# # firebase_app = initialize_app(cred)
# # db = firestore.client()

# # Arbitrary data for demonstration
# arbitrary_scores = [
#     {"username": "User1", "score": 8, "date_of_creation": "2023-09-15"},
#     {"username": "User2", "score": 7, "date_of_creation": "2023-09-14"},
#     {"username": "User3", "score": 6, "date_of_creation": "2023-09-13"},
#     {"username": "User4", "score": 5, "date_of_creation": "2023-09-12"},
# ]

# # Store arbitrary scores in Firestore (for demonstration)
# # scores_collection = db.collection("scores")
# # for score_data in arbitrary_scores:
# #     scores_collection.add(score_data)

# # # Retrieve Scores from Firestore
# # scores_query = scores_collection.order_by("date_of_creation", direction=firestore.Query.DESCENDING).limit(10)
# # scores = scores_query.stream()

# # score_data = []
# # for score in scores:
# #     data = score.to_dict()
# #     score_data.append(data)

# # Create a DataFrame
# df_scores = pd.DataFrame(arbitrary_scores)

# # Best Score Card
# best_score = df_scores["score"].max()
# st.subheader("My Scores")
# (
#     col1,
#     col2,
# ) = st.columns([1, 1], gap="small")

# col1.metric(
#     "**Best Score**",
#     value=best_score,
# )

# col2.metric(
#     "**Recent Score**",
#     value=5,
# )
# style_metric_cards(border_radius_px=2)

# # Create a Plotly chart displaying scores over time
# fig = px.line(df_scores, x="date_of_creation", y="score", title="Scores Over Time")
# st.plotly_chart(fig)


# # Leaderboard Card
# st.subheader("Leaderboard")
# st.dataframe(df_scores[["username", "score"]].head(5))

# # Footer
# st.write("© 2023 YourAppName. All rights reserved.")