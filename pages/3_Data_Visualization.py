import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_dynamic_filters import DynamicFilters
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
st.info(
    "You can filter the dataset to any combination of the following to slice and dice the visuals. All visuals refresh based on the multi-select input boxes.",
    icon="✍️",
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
df['Certified Degenerate Bet'] = (df["Certified Degenerate Bet"]).str.title().astype(str)

st.session_state.df = df

# ###########################################################################
# Page Filters
# ###########################################################################
bet_logger_dynamic_filters = DynamicFilters(
    df=df,
    filters=['Gambler Name', 'Bet Status', 'Bet Sport', 'Bet Date', 'Bet Category', 'Certified Degenerate Bet'],
    filters_name='bet_logger'
)
bet_logger_dynamic_filters.display_filters(location='sidebar', num_columns=2, gap='small')

# save filtered df as new variable
filter_df = bet_logger_dynamic_filters.filter_df()
source = filter_df

# ###########################################################################
# Show some metrics and charts
# ###########################################################################
st.header("Statistics & Data Visualization")
st.write("#### Bet Win vs. Loss Totals")
status_counts = filter_df['Bet Status'].value_counts().reset_index()
status_counts.columns = ['Bet Status', 'Count']

# Build Altair pie chart
pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Bet Status", type="nominal"),
    tooltip=["Bet Status", "Count"]
).properties(
    width="container",
    title="Wins vs Losses"
)

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(pie, theme="streamlit", use_container_width=True)
with tab2:
        st.altair_chart(pie, theme=None, use_container_width=True)

st.divider()

st.write("#### Bet Total Risk & Win Amounts Totals By Date")
st.info(
    "Data is restricted to the month selected in the selection box below. This reduces the clutter of the visual and maintains readability of data.",
    icon="⚠️",
)
filter_df['Bet Date'] = pd.to_datetime(filter_df['Bet Date'])
filter_df['Year-Month'] = filter_df['Bet Date'].dt.to_period('M').astype(str)

# Streamlit dropdown to select month
available_months = sorted(filter_df['Year-Month'].unique(), reverse=True)
selected_month = st.selectbox("Select Month:", available_months)

filtered_month_df = filter_df[filter_df['Year-Month'] == selected_month]

agg_df = (
    filtered_month_df
    .groupby('Bet Date')[['Bet Amount', 'Bet Net Win Amount']]
    .sum()
    .reset_index()
)

# Melt into long format for side-by-side bars
melted_df = agg_df.melt(
    id_vars='Bet Date',
    value_vars=['Bet Amount', 'Bet Net Win Amount'],
    var_name='Metric',
    value_name='Amount'
)

# Altair grouped horizontal bar chart
bar_chart = alt.Chart(melted_df).mark_bar().encode(
    column=alt.Column('Bet Date', spacing=5, header=alt.Header(labelOrient="bottom", labelAngle=50, labelPadding=75, labelFontSize=12)),
    x=alt.X('Metric', sort=['Bet Amount', 'Bet Net Win Amount'], axis=None),
    y=alt.Y('Amount', title='Amount'),
    color=alt.Color('Metric:N', title='Metric')
).properties(
    title='Bet Amount vs Net Win Amount by Date',
    width=30,
).interactive()

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(bar_chart, theme="streamlit", use_container_width=False)
with tab2:
    st.altair_chart(bar_chart, theme=None, use_container_width=False)

st.divider()

st.write("#### Bet Type Totals")
status_counts = filter_df['Bet Type'].value_counts().reset_index()
status_counts.columns = ['Bet Type', 'Count']

# Build Altair pie chart
pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Bet Type", type="nominal"),
    tooltip=["Bet Type", "Count"]
).properties(
    width="container",
    title="Bets Placed By Type"
)

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(pie, theme="streamlit", use_container_width=True)
with tab2:
        st.altair_chart(pie, theme=None, use_container_width=True)

st.divider()

st.write("#### Bet Sport Totals")
status_counts = filter_df['Bet Sport'].value_counts().reset_index()
status_counts.columns = ['Bet Sport', 'Count']

# Build Altair pie chart
pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Bet Sport", type="nominal"),
    tooltip=["Bet Sport", "Count"]
).properties(
    width="container",
    title="Bets Placed By Sport"
)

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(pie, theme="streamlit", use_container_width=True)
with tab2:
        st.altair_chart(pie, theme=None, use_container_width=True)

st.divider()

st.write("#### Bet Sportsbook Totals")
status_counts = filter_df['Sportsbook Name'].value_counts().reset_index()
status_counts.columns = ['Sportsbook Name', 'Count']

# Build Altair pie chart
pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Sportsbook Name", type="nominal"),
    tooltip=["Sportsbook Name", "Count"]
).properties(
    width="container",
    title="Bets Placed By Sportsbooks"
)

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(pie, theme="streamlit", use_container_width=True)
with tab2:
        st.altair_chart(pie, theme=None, use_container_width=True)

st.divider()

st.write("#### Certified Degenerate Bet Totals")
status_counts = filter_df['Certified Degenerate Bet'].value_counts().reset_index()
status_counts.columns = ['Certified Degenerate Bet', 'Count']

# Build Altair pie chart
pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Certified Degenerate Bet", type="nominal"),
    tooltip=["Certified Degenerate Bet", "Count"]
).properties(
    width="container",
    title="Certified Degenerate Bet Totals"
)

tab1, tab2 = st.tabs(["Streamlit theme", "Altair theme"])
with tab1:
    st.altair_chart(pie, theme="streamlit", use_container_width=True)
with tab2:
        st.altair_chart(pie, theme=None, use_container_width=True)

st.divider()