from datetime import datetime
import pytz
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
import time

# ###########################################################################
# Show app title and description.
# ###########################################################################
st.set_page_config(page_title="Bet Logger", page_icon="📒", layout="wide")
st.title("📒 Bet Logger 📒")
st.write(
    """
    Add a new bet slip to the archive.
    """
)
st.divider()

# ###########################################################################
# Create a connection object.
# Save the dataframe in session state (a dictionary-like object that persists across page runs). This ensures our data is persisted when the app updates.
# ###########################################################################
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

sheet_name = "Gamblers Anonymous Streamlit"
tab_name = "Master"

gc = gspread.service_account_from_dict(dict(st.secrets["gsheets"]))
# gc = gspread.service_account(filename="secrets/google-credentials.json")
google_sheet = gc.open(sheet_name)
google_worksheet = google_sheet.worksheet(tab_name)

# Convert to datetime.date
df['Bet Date'] = pd.to_datetime(df['Bet Date']).dt.date
df['Bet Odds'] = df["Bet Odds"].astype(str)
df['Certified Degenerate Bet'] = (df["Certified Degenerate Bet"]).str.title()

st.session_state.df = df

# ###########################################################################
# Generate date default in CST
# ###########################################################################
cst_na = pytz.timezone('America/Chicago')
datetime_cst_na = datetime.now(cst_na).date() 

# ###########################################################################
# selectbox Lists
# ###########################################################################
sportsbook_selectbox = ["Prizepicks", "Underdog", "Fliff", "Sleeper", "Chalkboard", "Boom Fantasy", "Potawatomi", "ParlayPlay", "FanDuel", "ProphetX", "Thrillz", "Rebet", "Novig"]
gambler_selectbox = ["Alex Hennes", "Ty Mallo", "Bryan Driebel", "Dustin Wendegatz"]
status_selectbox = ["Placed", "Win", "Loss", "Push", "Reboot"]
risk_type_selectbox = ["Cash", "Promotion"]
bet_type_selectbox = ["Straight", "Parlay", "Future"]
bet_category_selectbox = ["Prop", "Moneyline", "Spread", "Totals", "Mixed"]
bet_sport_selectbox = ["Baseball", "Football", "Basketball", "Hockey", "Tennis", "Soccer", "Golf", "Other"]
yes_no = ["No", "Yes"]

# ###########################################################################
# Show a form to add a new bet slip.
# We're adding bets via an `st.form` and some input widgets. If widgets are used in a form, the app will only rerun once the submit button is pressed.
# ###########################################################################
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'validation_messages' not in st.session_state:
    st.session_state.validation_messages = []

st.header("Log a New Bet Slip")
st.info(
    "You can add a new bet slip by entering information into the form below. If a bet result and payout becomes known, please use the table below and sort by bet status to find \"Placed\" bet slips.",
    icon="✍️",
)
with st.form("add_bet_slip_form"):
    # entry form
    gambler = st.selectbox(
        "Gambler Name"
        ,gambler_selectbox
        ,index=None
        ,placeholder="Select gambler name..."
    )
    bet_date = st.date_input(
        "Bet Date"
        ,value=datetime_cst_na
    )
    status = st.selectbox(
        "Bet Status"
        ,status_selectbox
        ,index=None
        ,placeholder="Select bet status..."
    )
    sportsbook = st.selectbox(
        "Sportsbook Name"
        ,sportsbook_selectbox
        ,index=None
        ,placeholder="Select sportsbook name..."
    )
    risk_type = st.selectbox(
        "Bet Risk Type"
        ,risk_type_selectbox
        ,index=None
        ,placeholder="Select bet risk type...")
    bet_type = st.selectbox(
        "Bet Type"
        ,bet_type_selectbox
        ,index=None
        ,placeholder="Select bet type..."
    )
    bet_category = st.selectbox(
        "Bet Category"
        ,bet_category_selectbox
        ,index=None
        ,placeholder="Select bet category..."
    )
    bet_sport = st.selectbox(
        "Bet Sport"
        ,bet_sport_selectbox
        ,index=None
        ,placeholder="Select bet sport(s)..."
    )
    bet_amount = st.number_input(
        "Bet Amount"
        ,format="%.2f"
        ,min_value=0.00
        ,placeholder="($USD) If a risk free promo bet, enter 0..."
        ,value=0.00
    )
    bet_promo_amount = st.number_input(
        "Bet Promotion Amount"
        ,format="%.2f"
        ,min_value=0.00
        ,value=0.00
    )
    bet_payout_amount = st.number_input(
        "Bet Payout Amount"
        ,format="%.2f"
        ,min_value=0.00
        ,value=0.00
    )
    bet_net_win_amount = st.number_input(
        "Bet Net Win Amount"
        ,format="%.2f"
        ,min_value=0.00
        ,value=0.00
    )
    bet_odds = st.text_input(
        "Bet Odds"
        ,placeholder="Enter bet odds, including +/-"
    )
    bet_team_player = st.text_area(
        "Bet Team/Player(s)"
        ,placeholder="Enter bet subject(s) using one per line")
    bet_stat = st.text_area(
        "Bet Statistic(s)"
        ,placeholder="Enter bet statistic(s) using one per line")
    bet_game = st.text_area(
        "Bet Game(s)"
        ,placeholder="Enter bet game(s) using one per line"
    )
    degen_bet = st.selectbox(
        "Certified Degenerate Bet"
        ,yes_no
    )
    notes = st.text_area(
        "Bet Notes"
        ,placeholder="Enter bet notes such as FLEX FRIDAY 💪, PAYOUT BOOST 🚀, TACO TUESDAY 🌮, DISCOUNT DOGS 🌭, etc."
    )
    
    submitted = st.form_submit_button("Submit")

if submitted:
    required_fields = {
        "Gambler Name": gambler,
        "Bet Status": status,
        "Sportsbook Name": sportsbook,
        "Bet Risk Type": risk_type,
        "Bet Type": bet_type,
        "Bet Category": bet_category,
        "Bet Sport": bet_sport,
        "Bet Odds": bet_odds,
        "Bet Team/Player(s)": bet_team_player,
        "Bet Statistic(s)": bet_stat,
        "Bet Game(s)": bet_game,
        "Certified Degenerate Bet": degen_bet,
    }

    # Check for any missing or empty required fields
    missing_fields = [name for name, value in required_fields.items() if not value]

    if missing_fields:
        st.error(f"Please complete all required fields before submitting: {', '.join(missing_fields)}")
    else:
        df_with_submitted = pd.DataFrame(
            [
                {
                    "Gambler Name": gambler,
                    "Sportsbook Name": sportsbook,
                    "Bet Status": status,
                    "Bet Risk Type": risk_type,
                    "Bet Type": bet_type,
                    "Bet Cateogry": bet_category,
                    "Bet Sport": bet_sport,
                    "Bet Date": bet_date,
                    "Bet Amount": bet_amount,
                    "Bet Promotion Amount": bet_promo_amount,
                    "Bet Payout Amount": bet_payout_amount,
                    "Bet Net Win Amount": bet_net_win_amount,
                    "Bet Odds": bet_odds,
                    "Bet Team/Player(s)": bet_team_player,
                    "Bet Statistic(s)": bet_stat,
                    "Bet Game(s)": bet_game,
                    "Certified Degenerate Bet": degen_bet,
                    "Notes": notes,
                }
            ]
        )

        # ###########################################################################
        # Show a success message & combine df
        # ###########################################################################
        st.success("🤑 Bet slip submitted! Details can be found below.")
        st.dataframe(df_with_submitted, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([df_with_submitted, st.session_state.df], axis=0)

        # ###########################################################################
        # Write new bet slip contents to sheet
        # ###########################################################################    
        df_with_submitted["Bet Date"] = df_with_submitted["Bet Date"].astype(str)
        df_with_submitted = df_with_submitted.fillna("N/A")

        google_worksheet.append_rows(df_with_submitted.values.tolist(), value_input_option="USER_ENTERED")
    


# ###########################################################################
# Show section to view and edit existing bets in a table.
# ###########################################################################
st.divider()
st.header("Update an existing bet")
st.info(
    "You can edit the bet slips by double clicking on a cell. The table is sortable by clicking on column headers.",
    icon="✍️",
)


# ###########################################################################
# Show the bets dataframe with `st.data_editor`. This lets the user edit the table cells. The edited data is returned as a new dataframe.
# ###########################################################################
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Gambler Name": st.column_config.SelectboxColumn(
            "Gambler Name",
            help="Gambler Name",
            options=gambler_selectbox,
            required=True,
        ),
        "Sportsbook Name": st.column_config.SelectboxColumn(
            "Sportsbook Name",
            help="Sportsbook Name",
            options=sportsbook_selectbox,
            required=True,
        ),  
        "Bet Status": st.column_config.SelectboxColumn(
            "Bet Status",
            help="Bet Status",
            options=status_selectbox,
            required=True,
        ), 
        "Bet Risk Type": st.column_config.SelectboxColumn(
            "Bet Risk Type",
            help="Bet Risk Type",
            options=risk_type_selectbox,
            required=True,
        ), 
        "Bet Type": st.column_config.SelectboxColumn(
            "Bet Type",
            help="Bet Type",
            options=bet_type_selectbox,
            required=True,
        ), 
        "Bet Category": st.column_config.SelectboxColumn(
            "Bet Category",
            help="Bet Category",
            options=bet_category_selectbox,
            required=True,
        ), 
        "Bet Sport": st.column_config.SelectboxColumn(
            "Bet Sport",
            help="Bet Sport (Primary)",
            options=bet_sport_selectbox,
            required=True,
        ), 
        "Bet Date": st.column_config.DateColumn(
            "Bet Date",
            help="Bet Date",
            required=True,
        ), 
        "Bet Amount": st.column_config.NumberColumn(
            "Bet Amount",
            help="If a risk free promo bet, enter 0...",
            min_value=0,
            format="dollar",
            required=True,
        ), 
        "Bet Promotion Amount": st.column_config.NumberColumn(
            "Bet Promotion Amount",
            help="If a risk free promo bet, enter value here. Otherwise enter 0...",
            min_value=0,
            format="dollar",
            required=True,
        ), 
        "Bet Payout Amount": st.column_config.NumberColumn(
            "Bet Payout Amount",
            help="If the bet is settled, enter total payout amount. Otherwise enter 0 to update later...",
            min_value=0,
            format="dollar",
            required=True,
        ), 
        "Bet Net Win Amount": st.column_config.NumberColumn(
            "Bet Net Win Amount",
            help="If the bet pays any nonzero amount, enter total payout amount. Otherwsie enter 0...",
            min_value=0,
            format="dollar",
            required=True,
        ), 
        "Bet Odds": st.column_config.NumberColumn(
            "Bet Odds",
            help="Enter bet odds, including +/- (American)",
            required=True,
        ), 
        "Bet Team/Player(s)": st.column_config.TextColumn(
            "Bet Team/Player(s)",
            help="Enter bet subject(s) using a new line for each leg (alt + enter)...",
            required=True,
        ), 
        "Bet Statistic(s)": st.column_config.TextColumn(
            "Bet Statistic(s)",
            help="Enter bet statistic(s) using a new line for each leg (alt + enter)...",
            required=True,
        ), 
        "Bet Game(s)": st.column_config.TextColumn(
            "Bet Game(s)",
            help="Enter bet game(s) using a new line for each leg (alt + enter)...",
            required=True,
        ),   
        "Certified Degenerate Bet": st.column_config.SelectboxColumn(
            "Certified Degenerate Bet",
            options=yes_no,
            help="(Generally +1000 or higher)",
            required=True,
        ), 
        "Bet Notes": st.column_config.TextColumn(
            "Bet Notes",
            help="Enter bet notes such as FLEX FRIDAY 💪, PAYOUT BOOST 🚀, TACO TUESDAY 🌮, DISCOUNT DOGS 🌭, etc...",
            required=True,
        ),                                                                                                                                     
    },
    # Disable editing
    disabled=[],
)
st.session_state.df = edited_df

# ###########################################################################
#  Write updated bet slip contents to sheet
# ###########################################################################
submit_update = st.button(label="Submit Update(s)",
            type="primary",
            icon="🗳️",
        )

if submit_update:
    df_update_existing_bet = edited_df
    df_update_existing_bet["Bet Date"] = df_update_existing_bet["Bet Date"].astype(str)
    df_update_existing_bet = df_update_existing_bet.fillna("N/A")

    # Create a backup as the update process is truncate-load
    data = google_worksheet.get_all_values()
    # Create or get backup tab
    backup_ws = google_sheet.worksheet("Backup")
    backup_ws.clear()
    backup_ws.update("A1", data)

    # google_worksheet.clear()
    google_worksheet.update("A1",
                            [df_update_existing_bet.columns.tolist()] + df_update_existing_bet.values.tolist(),
                             value_input_option="RAW"
                        )
    with st.empty():
        st.success("✅ Successfully wrote bet update(s)!")
        time.sleep(5)
        st.write("")

st.divider()