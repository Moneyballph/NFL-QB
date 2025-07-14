
import streamlit as st

st.set_page_config(page_title="Moneyball Phil: NFL Prop Simulator (v2)", layout="centered")

st.title("🏈 Moneyball Phil: NFL Prop Simulator (v2)")
st.markdown("_Simulate Under 1.5 Passing TDs and Alt Over Passing Yards for any QB_")

# Quarterback and Opponent Info
qb_name = st.text_input("Quarterback Name")
opponent_team = st.text_input("Opponent Team")

# Passing Yards Line (Standard)
st.subheader("📈 Standard Passing Yards Prop")
passing_yards_line = st.number_input("Passing Yards Line", value=225)
odds_over_yards = st.number_input("Odds for Over (Standard Yards)", value=-110)
odds_under_yards = st.number_input("Odds for Under (Standard Yards)", value=-120)

# Alt Over Yards
st.subheader("📊 Alt Over Passing Yards Prop")
alt_yards_line = st.number_input("Alt Over Yards Line", value=199)
alt_yards_odds = st.number_input("Odds for Alt Over Line", value=-145)

# Passing TDs
st.subheader("🏈 Passing Touchdowns Prop")
passing_td_line = st.number_input("Passing TD Line", value=1.5)
odds_under_td = st.number_input("Odds for Under TDs", value=100)

# QB and Defense Stats
st.subheader("📊 Statistical Inputs")
qb_yds_pg = st.number_input("QB Yards/Game", value=240)
qb_td_pg = st.number_input("QB TD/Game", value=1.4)
pass_att_pg = st.number_input("Pass Attempts/Game", value=31.5)
def_yds_allowed = st.number_input("Defense Yards Allowed/Game", value=230)
def_tds_allowed = st.number_input("Defense Pass TDs/Game", value=1.2)

# Simulate Button
if st.button("🎯 Simulate Player"):
    st.success("Simulation complete for " + qb_name)
    st.write("🚧 Probability and EV logic will be implemented in the next full version.")
    st.dataframe({
        "Player": [qb_name],
        "Line (Yds)": [passing_yards_line],
        "True % Over": ["TBD"],
        "True % Under": ["TBD"],
        "Implied % Over": ["TBD"],
        "Implied % Under": ["TBD"],
        "EV % Over": ["TBD"],
        "EV % Under": ["TBD"],
        "Tier": ["TBD"]
    })
