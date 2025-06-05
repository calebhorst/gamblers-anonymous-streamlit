import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_dynamic_filters import DynamicFilters
from utils import filter_dataframe

# ###########################################################################
# Show app title and description.
# ###########################################################################
st.set_page_config(page_title="Data Visualization", page_icon="📊", layout="wide")
st.title("📊 Data Visualization 📊")
st.write(
    """
    The :red[banned] players list. Contact a site administrator to review your banned player and/or prop submission.
    """
)

st.divider()

st.info(
    "Not all of us can be money like Sandy Alcantara, thats what makes him the 🐐",
    icon="✍️",
)

# ###########################################################################
# Hard coding because this is very stale and I'm lazy
# ###########################################################################
data = {
    "Player and/or Prop": [
        "Bam Adebayo",
        ],
    "Ban Date": [2024,
        ],
    "Ban Reason": [
        "The OG. Fail fast, fail often!",
    ]
}
df = pd.DataFrame(data)

st.session_state.df = df

# ###########################################################################
# User input for filtering dataframe
# ###########################################################################
st.dataframe(filter_dataframe(df))
st.divider()