import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Hospital Patient Flow Dashboard", layout="wide")
st.title("🏥 Real-Time Patient Flow Dashboard")

DATABASE_URL = "postgresql://kafka_user:kafka_password@localhost:5433/kafka_db"


@st.cache_resource
def get_engine(url):
    return create_engine(url, pool_pre_ping=True)


engine = get_engine(DATABASE_URL)


def load_data(status_filter=None, limit=200):
    base_query = "SELECT * FROM patient_events"
    params = {}

    if status_filter and status_filter != "All":
        base_query += " WHERE status = :status"
        params["status"] = status_filter

    base_query += " ORDER BY event_id DESC LIMIT :limit"
    params["limit"] = limit

    return pd.read_sql_query(text(base_query), con=engine.connect(), params=params)


# Sidebar
status_options = [
    "All",
    "Waiting",
    "In Treatment",
    "Discharged",
    "Left Without Being Seen",
]
selected_status = st.sidebar.selectbox("Filter by Status", status_options)
update_interval = st.sidebar.slider("Refresh interval (s)", 2, 20, 5)
limit_records = st.sidebar.number_input("Records to load", 50, 2000, 200, step=50)

placeholder = st.empty()

while True:
    df = load_data(selected_status, limit_records)

    with placeholder.container():

        if df.empty:
            st.warning("Waiting for patient events...")
            time.sleep(update_interval)
            continue

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # KPIs
        total_events = len(df)
        avg_waiting = df["waiting_time"].mean()
        avg_triage = df["triage_level"].mean()
        in_treatment = len(df[df["status"] == "In Treatment"])
        discharged = len(df[df["status"] == "Discharged"])

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Events", total_events)
        k2.metric("Avg Waiting Time (min)", f"{avg_waiting:.1f}")
        k3.metric("Avg Triage Level (1-5)", f"{avg_triage:.2f}")
        k4.metric("In Treatment", in_treatment)
        k5.metric("Discharged", discharged)

        st.markdown("### Recent Events")
        st.dataframe(df.head(10), use_container_width=True)

        # Charts
        fig_wait = px.bar(
            df.groupby("specialty")["waiting_time"].mean().reset_index(),
            x="specialty",
            y="waiting_time",
            title="Average Waiting Time by Specialty",
        )

        fig_triage = px.histogram(
            df, x="triage_level", title="Distribution of Triage Levels", nbins=5
        )

        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_wait, use_container_width=True)
        col2.plotly_chart(fig_triage, use_container_width=True)

        st.caption(f"Updated at {datetime.now().isoformat()}")

    time.sleep(update_interval)
