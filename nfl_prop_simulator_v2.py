
import streamlit as st

st.set_page_config(page_title="🏈 Moneyball Phil: NFL Prop Simulator", layout="centered")

st.title("🏈 Moneyball Phil: NFL Prop Simulator (v2)")
st.markdown("Simulate Under 1.5 Passing TDs and Alt Over/Under Passing Yards for any QB based on historical or projected stats.")

with st.form("nfl_sim_form"):
    qb_name = st.text_input("Quarterback Name")
    opponent = st.text_input("Opponent Team")
    
    passing_yards_line = st.number_input("Passing Yards Line", value=225)
    odds_passing_yards_over = st.number_input("Odds for Passing Yards Over", value=-110)
    odds_passing_yards_under = st.number_input("Odds for Passing Yards Under", value=-110)
    
    alt_yards_line = st.number_input("Alt Over Yards Line", value=199)
    odds_alt_line = st.number_input("Odds for Alt Over Line", value=-145)
    
    td_line = st.number_input("Passing TD Line", value=1.5)
    odds_td_under = st.number_input("Odds for Under TDs", value=100)
    
    qb_yards = st.number_input("QB Yards/Game", value=240)
    qb_tds = st.number_input("QB TD/Game", value=1.40)
    pass_attempts = st.number_input("Pass Attempts/Game", value=31.5)
    
    def_yards_allowed = st.number_input("Defense Yards Allowed/Game", value=230)
    def_pass_tds = st.number_input("Defense Pass TDs/Game", value=1.20)
    
    submitted = st.form_submit_button("Simulate Player")

if submitted:
    st.subheader(f"Simulation Results for {qb_name} vs {opponent}")

    # Dummy placeholders for results (replace with real logic later)
    st.markdown("### 📊 Passing Yards Line")
    st.write("True Probability (Over): 54.3%")
    st.write("True Probability (Under): 45.7%")
    st.write("Implied Probability (Over): 52.4%")
    st.write("EV% (Over): +3.6%")
    
    st.markdown("### 📊 Alt Over Yards Line")
    st.write("True Probability: 59.8%")
    st.write("Implied Probability: 59.2%")
    st.write("EV%: +0.6%")
    
    st.markdown("### 📊 Under 1.5 Passing TDs")
    st.write("True Probability: 51.0%")
    st.write("Implied Probability: 50.0%")
    st.write("EV%: +1.0%")
