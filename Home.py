import streamlit as st

# ###########################################################################
# Show app title and description.
# ###########################################################################
st.set_page_config(page_title="Gamblers Anonymous", page_icon="💸", layout="wide")
st.title("💸 Gamblers Anonymous 💸")
st.divider()
st.markdown(
    """
    ## :green[Welcome to the home of degenerate parlays!]
    **👈 Select a page from the sidebar** for more information
    - Logging a new bet using the *Bet Logger*
    - Reviewing historical bet data, beginning from `2025-01-01` and onwards
    - Visualizing betting data to refine betting analysis
    
    ## :green[The Basics]
    ### Aren't you addicted to gambling?
        No. We are all emotionless, calculating, and economically rational individuals.
    ### What's the number for gambling help?
        1-800-GAMBLER
    ### Do you have a code of ethics?
        Remember to read and adhere to the "Gamblers Manifesto"!
    ### Why were you banned from PrizePicks?
        We don't talk about that anymore. The charges were rescinded.
    ### What bets should I place for a guaranteed win?
        1. Obi Toppin - Over 4.5 R+A
        2. Sanday Alcantara - Under 17.5 Pitching Outs            
    """
)
st.divider()