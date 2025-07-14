
import streamlit as st
import math

# Set page config
st.set_page_config(page_title="🏈 Moneyball Phil: NFL Prop Simulator", layout="centered")

# Background Image Setup
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("football_background.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🏈 Moneyball Phil: NFL Prop Simulator (Final Version)")

st.markdown("Simulate Under 1.5 Passing TDs and Alt Over Passing Yards for any QB based on historical or projected stats.")

# Input Fields
qb_name = st.text_input("Quarterback Name")
opponent = st.text_input("Opponent Team")

st.subheader("📊 Passing Yards Props")
standard_line = st.number_input("Standard Passing Yards Line", value=225)
std_odds_over = st.number_input("Odds for Over (Standard Line)", value=-110)
std_odds_under = st.number_input("Odds for Under (Standard Line)", value=-110)

alt_line = st.number_input("Alt Over Yards Line", value=199)
alt_odds = st.number_input("Odds for Alt Over Line", value=-145)

st.subheader("🎯 Touchdown Props")
td_line = st.number_input("Passing TD Line", value=1.5, step=0.5)
odds_td_under = st.number_input("Odds for Under TDs", value=100)

st.subheader("📈 QB & Defense Stats")
qb_yards = st.number_input("QB Yards/Game", value=240.0)
qb_tds = st.number_input("QB TD/Game", value=1.4)
qb_att = st.number_input("Pass Attempts/Game", value=31.5)

def_yards = st.number_input("Defense Yards Allowed/Game", value=230.0)
def_tds = st.number_input("Defense Pass TDs/Game", value=1.2)

def calc_true_prob(qb_stat, def_stat):
    return max(0.01, min(0.99, (qb_stat + def_stat) / 2 / (qb_stat + def_stat + 100)))  # Simplified logistic model

def calc_ev(true_prob, odds):
    if odds > 0:
        implied = 100 / (odds + 100)
    else:
        implied = abs(odds) / (abs(odds) + 100)
    ev = round((true_prob - implied) * 100, 2)
    implied_percent = round(implied * 100, 2)
    return round(true_prob * 100, 2), implied_percent, ev

def get_tier(prob):
    if prob >= 80:
        return "🟢 Elite"
    elif prob >= 65:
        return "🟡 Strong"
    elif prob >= 50:
        return "🟠 Moderate"
    else:
        return "🔴 Risky"

# Simulation Logic
if st.button("Simulate Player"):
    st.subheader("📋 Player Prop Simulation Results")

    std_true_over = (qb_yards + def_yards) / 2
    std_prob_over = min(0.99, max(0.01, std_true_over / (standard_line + 60)))
    std_prob_under = 1 - std_prob_over

    alt_prob_over = min(0.99, max(0.01, std_true_over / (alt_line + 60)))

    td_prob_under = min(0.99, max(0.01, 1 - ((qb_tds + def_tds) / 2 / (td_line + 1.25))))

    # EV calculations
    std_over_true, std_over_imp, std_over_ev = calc_ev(std_prob_over, std_odds_over)
    std_under_true, std_under_imp, std_under_ev = calc_ev(std_prob_under, std_odds_under)
    alt_true, alt_imp, alt_ev = calc_ev(alt_prob_over, alt_odds)
    td_true, td_imp, td_ev = calc_ev(td_prob_under, odds_td_under)

    # Display table
    import pandas as pd
    results = pd.DataFrame([
        {"Prop": "Standard Over", "True Probability": f"{std_over_true}%", "Implied Probability": f"{std_over_imp}%", "EV %": f"{std_over_ev}%", "Tier": get_tier(std_over_true)},
        {"Prop": "Standard Under", "True Probability": f"{std_under_true}%", "Implied Probability": f"{std_under_imp}%", "EV %": f"{std_under_ev}%", "Tier": get_tier(std_under_true)},
        {"Prop": "Alt Over", "True Probability": f"{alt_true}%", "Implied Probability": f"{alt_imp}%", "EV %": f"{alt_ev}%", "Tier": get_tier(alt_true)},
        {"Prop": "Under TDs", "True Probability": f"{td_true}%", "Implied Probability": f"{td_imp}%", "EV %": f"{td_ev}%", "Tier": get_tier(td_true)}
    ])

    st.dataframe(results, use_container_width=True)
