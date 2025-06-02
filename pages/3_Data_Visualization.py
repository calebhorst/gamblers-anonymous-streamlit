from datetime import datetime
import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utils import filter_dataframe

# ###########################################################################
# Show app title and description.
# ###########################################################################
st.set_page_config(page_title="Data Visualization", page_icon="📊")
st.title("📊 Data Visualization 📊")
st.write(
    """
    Overall statistics and aggregate calculations for historical bet data.
    """
)
st.divider()

# ###########################################################################
# Create a connection object.
# Save the dataframe in session state (a dictionary-like object that persists across page runs). This ensures our data is persisted when the app updates.
# ###########################################################################
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()
# Convert to datetime.date
df['Bet Date'] = pd.to_datetime(df['Bet Date']).dt.date
df['Bet Odds'] = df["Bet Odds"].astype(str)

st.session_state.df = df

# ###########################################################################
# Show some metrics and charts about the ticket.
# ###########################################################################
st.header("Statistics & Data Visualization")

# Show metrics side by side using `st.columns` and `st.metric`.
# col1, col2, col3 = st.columns(3)
# num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
# col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
# col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
# col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# # Show two Altair charts using `st.altair_chart`.
# st.write("")
# st.write("##### Ticket status per month")
# status_plot = (
#     alt.Chart(edited_df)
#     .mark_bar()
#     .encode(
#         x="month(Date Submitted):O",
#         y="count():Q",
#         xOffset="Status:N",
#         color="Status:N",
#     )
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# st.write("##### Current ticket priorities")
# priority_plot = (
#     alt.Chart(edited_df)
#     .mark_arc()
#     .encode(theta="count():Q", color="Priority:N")
#     .properties(height=300)
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

st.divider()