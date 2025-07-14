
import streamlit as st
import numpy as np
from scipy.stats import norm, poisson

st.set_page_config(page_title="Moneyball Phil: NFL Prop Simulator (v3)", layout="centered")

st.title("🏈 Moneyball Phil: NFL Prop Simulator (v3)")
st.markdown("Simulate **Under 1.5 Passing TDs** and **Alt Over/Standard Yards** for any QB.")

# Input fields
qb_name = st.text_input("Quarterback Name")
opponent = st.text_input("Opponent Team")
passing_yards_line = st.number_input("Passing Yards Line", value=225)
odds_over_standard = st.number_input("Odds for Over (Standard Line)", value=-110)
odds_under_standard = st.number_input("Odds for Under (Standard Line)", value=-110)
alt_over_line = st.number_input("Alt Over Yards Line", value=199)
odds_alt_over = st.number_input("Odds for Alt Over Line", value=-145)
td_line = st.number_input("Passing TD Line", value=1.5, step=0.5)
odds_under_td = st.number_input("Odds for Under TDs", value=100)

# QB Stats
qb_yds_pg = st.number_input("QB Yards/Game", value=240)
qb_td_pg = st.number_input("QB TD/Game", value=1.40)
pass_attempts = st.number_input("Pass Attempts/Game", value=31.5)

# Defense Stats
def_yds_allowed = st.number_input("Defense Yards Allowed/Game", value=230)
def_td_allowed = st.number_input("Defense Pass TDs/Game", value=1.20)

def calculate_implied_prob(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)

def calculate_ev(true_prob, implied_prob):
    return round((true_prob - implied_prob) * 100, 2)

def simulate():
    if not qb_name or not opponent:
        st.warning("Please enter the QB name and opponent.")
        return

    # Estimate variance
    std_dev_yards = 35

    # Passing Yards Probability
    prob_over_std = 1 - norm.cdf(passing_yards_line, loc=qb_yds_pg, scale=std_dev_yards)
    prob_under_std = norm.cdf(passing_yards_line, loc=qb_yds_pg, scale=std_dev_yards)

    implied_over_std = calculate_implied_prob(odds_over_standard)
    implied_under_std = calculate_implied_prob(odds_under_standard)
    ev_over_std = calculate_ev(prob_over_std, implied_over_std)
    ev_under_std = calculate_ev(prob_under_std, implied_under_std)

    # Alt Over Line
    prob_alt_over = 1 - norm.cdf(alt_over_line, loc=qb_yds_pg, scale=std_dev_yards)
    implied_alt = calculate_implied_prob(odds_alt_over)
    ev_alt = calculate_ev(prob_alt_over, implied_alt)

    # Under TDs using Poisson model
    lambda_td = (qb_td_pg + def_td_allowed) / 2
    prob_under_td = poisson.cdf(1, mu=lambda_td)
    implied_td = calculate_implied_prob(odds_under_td)
    ev_td = calculate_ev(prob_under_td, implied_td)

    # Display Results
    st.subheader(f"📊 Simulation Results for {qb_name} vs {opponent}")

    st.markdown("### 🟦 Standard Passing Yards Line")
    st.write(f"**Over {passing_yards_line} Yards**: {prob_over_std:.2%} (EV: {ev_over_std}%)")
    st.write(f"**Under {passing_yards_line} Yards**: {prob_under_std:.2%} (EV: {ev_under_std}%)")

    st.markdown("### 🟩 Alt Over Line")
    st.write(f"**Over {alt_over_line} Yards**: {prob_alt_over:.2%} (EV: {ev_alt}%)")

    st.markdown("### 🔴 Under 1.5 Passing TDs")
    st.write(f"**Under 1.5 TDs**: {prob_under_td:.2%} (EV: {ev_td}%)")

if st.button("Simulate Player"):
    simulate()
