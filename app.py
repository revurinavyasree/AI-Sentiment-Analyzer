import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import matplotlib.pyplot as plt
import os

# Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Page Config
st.set_page_config(
    page_title="AI Sentiment Analyzer",
    page_icon="🧠",
    layout="wide"
)

# Title
st.title("🧠 AI Sentiment Analyzer Dashboard")
st.write("Analyze text sentiment using AI-powered NLP")

# User Input
text = st.text_area("Enter Text")

# Analyze Button
if st.button("Analyze"):

    if text.strip():

        result = analyzer.polarity_scores(text)
        score = result["compound"]

        if score >= 0.05:
            sentiment = "Positive 😊"
            st.success(sentiment)

        elif score <= -0.05:
            sentiment = "Negative 😡"
            st.error(sentiment)

        else:
            sentiment = "Neutral 😐"
            st.warning(sentiment)

        st.metric("Sentiment Score", round(score, 2))

        # Save History
        row = pd.DataFrame({
            "Time": [datetime.now()],
            "Text": [text],
            "Sentiment": [sentiment],
            "Score": [score]
        })

        if os.path.exists("history.csv") and os.path.getsize("history.csv") > 0:
            row.to_csv(
                "history.csv",
                mode="a",
                header=False,
                index=False
            )
        else:
            row.to_csv(
                "history.csv",
                index=False
            )

st.divider()

st.subheader("📜 Analysis History")

# Read History
if os.path.exists("history.csv") and os.path.getsize("history.csv") > 0:

    history = pd.read_csv("history.csv")

    # Sidebar Filter
    st.sidebar.header("Filters")

    selected = st.sidebar.selectbox(
        "Filter Sentiment",
        ["All", "Positive 😊", "Negative 😡", "Neutral 😐"]
    )

    if selected != "All":
        history = history[history["Sentiment"] == selected]

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Analyses",
        len(history)
    )

    col2.metric(
        "Average Score",
        round(history["Score"].mean(), 2)
    )

    positive_count = history["Sentiment"].str.contains("Positive").sum()

    positive_percentage = round(
        (positive_count / len(history)) * 100,
        1
    ) if len(history) > 0 else 0

    col3.metric(
        "Positive %",
        positive_percentage
    )

    # Table
    st.dataframe(history, width="stretch")

    # Download Button
    st.download_button(
        label="⬇ Download History CSV",
        data=history.to_csv(index=False),
        file_name="history.csv",
        mime="text/csv"
    )

    st.divider()

    # Pie Chart
    st.subheader("🥧 Sentiment Distribution")

    counts = history["Sentiment"].value_counts()

    fig1, ax1 = plt.subplots()

    ax1.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig1)

    # Bar Chart
    st.subheader("📊 Sentiment Count")

    st.bar_chart(counts)

else:
    st.info("No history yet. Analyze some text first.")