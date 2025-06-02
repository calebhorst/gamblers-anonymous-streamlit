from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utils import filter_dataframe

# ###########################################################################
# Show app title and description.
# ###########################################################################
st.set_page_config(page_title="Historical Bet Lookup", page_icon="🔎")
st.title("🔎 Historical Bet Lookup 🔎")
st.write(
    """
    A historical data lookup for all bets placed through the `Gamblers Anonymous` support group. Many :green[winners]! ... and even more :red[losers]!
    """
)

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
# Show section to view and edit existing bets in a table.
# ###########################################################################
st.header("Historical Bet Records")
st.write(f"Number of total bets placed: `{len(st.session_state.df)}`")

st.info(
    "You can filter the historical data by any dimension and/or attribute using the Add filters checkbox.",
    icon="✍️",
)

# ###########################################################################
# User input for filtering dataframe
# ###########################################################################
st.dataframe(filter_dataframe(df))