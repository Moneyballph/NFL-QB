
import streamlit as st
import pandas as pd
import math

# Set background
def set_bg():
    st.markdown(f'''
        <style>
        .stApp {
            background-image: url("backgrounds/nfl_field_bg.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
    ''', unsafe_allow_html=True)

set_bg()

st.title("🏈 Moneyball Phil: NFL Prop Simulator")

# Inputs
qb_name = st.text_input("Quarterback Name", "Mac Jones")
opponent = st.text_input("Opponent Team", "Cowboys")

st.subheader("📊 Passing Yards Props")
standard_line = st.number_input("Standard Passing Yards Line", value=212)
over_odds = st.number_input("Odds for Over (Standard Line)", value=-110)
under_odds = st.number_input("Odds for Under (Standard Line)", value=-120)

alt_line = st.number_input("Alt Over Yards Line", value=199)
alt_odds = st.number_input("Odds for Alt Over Line", value=-135)

st.subheader("🎯 Touchdown Props")
td_line = st.number_input("Passing TD Line", value=1.5)
td_under_odds = st.number_input("Odds for Under TDs", value=-105)

st.subheader("📈 QB & Defense Stats")
qb_ypg = st.number_input("QB Yards/Game", value=167.2)
qb_tdp = st.number_input("QB TD/Game", value=0.8)
qb_att = st.number_input("Pass Attempts/Game", value=26.2)
def_ypg = st.number_input("Defense Yards Allowed/Game", value=238.0)
def_tdp = st.number_input("Defense Pass TDs/Game", value=0.76)

def implied_prob(odds):
    return round(abs(odds) / (abs(odds) + 100), 4) if odds > 0 else round(100 / (abs(odds) + 100), 4)

def simulate_props(std_line, alt_line, td_line_val):
    std_over_prob = min(1.0, (qb_ypg + def_ypg) / (2 * std_line))
    std_under_prob = 1 - std_over_prob
    alt_over_prob = min(1.0, (qb_ypg + def_ypg) / (2 * alt_line))
    td_under_prob = 1 - min(1.0, (qb_tdp + def_tdp) / (2 * td_line_val))

    return [
        ("Standard Over", std_over_prob, implied_prob(over_odds)),
        ("Standard Under", std_under_prob, implied_prob(under_odds)),
        ("Alt Over", alt_over_prob, implied_prob(alt_odds)),
        (f"Under {td_line_val} TDs", td_under_prob, implied_prob(td_under_odds)),
    ]

def calculate_ev(true_prob, implied_prob):
    return round((true_prob - implied_prob) * 100, 2)

def get_tier(ev):
    if ev >= 40:
        return "🟢 Elite"
    elif ev >= 15:
        return "🟡 Strong"
    elif ev >= 0:
        return "🟠 Moderate"
    else:
        return "🔴 Risky"

if st.button("Simulate Props"):
    st.subheader("📋 Player Prop Simulation Results")
    results = simulate_props(standard_line, alt_line, td_line)
    table = []
    for label, true_p, implied_p in results:
        ev = calculate_ev(true_p, implied_p)
        tier = get_tier(ev)
        table.append([label, f"{true_p*100:.2f}%", f"{implied_p*100:.2f}%", f"{ev}%", tier])

    df = pd.DataFrame(table, columns=["Prop", "True Probability", "Implied Probability", "EV %", "Tier"])
    st.dataframe(df)
