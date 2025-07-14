
import streamlit as st
import math

st.set_page_config(page_title="🏈 Moneyball Phil: NFL Prop Simulator", layout="centered")

st.title("🏈 Moneyball Phil: NFL Prop Simulator (v1.2)")
st.markdown("Simulate **Under 1.5 Passing TDs** and **Alt/Standard Over Passing Yards** props for any QB.")

st.header("📋 Input Player & Matchup Data")

col1, col2 = st.columns(2)
with col1:
    qb_name = st.text_input("Quarterback Name", value="Kenny Picket")
    opponent_team = st.text_input("Opponent Team", value="Texans")

st.subheader("📊 Passing Yards Props")
col3, col4, col5 = st.columns(3)
with col3:
    standard_yds_line = st.number_input("Standard Passing Yards Line", value=210)
with col4:
    odds_over_std = st.number_input("Odds for Over (Standard Line)", value=-115)
with col5:
    odds_under_std = st.number_input("Odds for Under (Standard Line)", value=-105)

col6, col7 = st.columns(2)
with col6:
    alt_yds_line = st.number_input("Alt Over Yards Line", value=199)
with col7:
    odds_alt_over = st.number_input("Odds for Alt Over Line", value=-145)

st.subheader("🎯 Touchdown Props")
col8, col9 = st.columns(2)
with col8:
    td_line = st.number_input("Passing TD Line", value=1.5)
with col9:
    odds_under_tds = st.number_input("Odds for Under TDs", value=100)

st.subheader("📈 QB & Defense Stats")
col10, col11, col12 = st.columns(3)
with col10:
    qb_yards = st.number_input("QB Yards/Game", value=188.0)
with col11:
    qb_td = st.number_input("QB TD/Game", value=0.7)
with col12:
    pass_attempts = st.number_input("Pass Attempts/Game", value=27.6)

col13, col14 = st.columns(2)
with col13:
    def_yds_allowed = st.number_input("Defense Yards Allowed/Game", value=237.0)
with col14:
    def_td_allowed = st.number_input("Defense Pass TDs/Game", value=1.1)

def implied_prob(odds):
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

def ev_calc(true_prob, odds):
    imp_prob = implied_prob(odds)
    return round((true_prob - imp_prob) * 100, 2)

def get_tier(prob):
    if prob >= 80:
        return "🟢 Elite"
    elif prob >= 65:
        return "🟡 Strong"
    elif prob >= 50:
        return "🟠 Moderate"
    else:
        return "🔴 Risky"

def binomial_probability(k, n, p):
    comb = math.comb(n, k)
    return comb * (p ** k) * ((1 - p) ** (n - k))

if st.button("🎯 Simulate Player"):
    st.header("📋 Player Prop Simulation Results")
    avg_yds = (qb_yards + def_yds_allowed) / 2
    avg_tds = (qb_td + def_td_allowed) / 2
    n_attempts = pass_attempts
    p_per_attempt = avg_tds / n_attempts if n_attempts > 0 else 0

    # Props
    std_over_prob = round((1 - math.exp(-((avg_yds - standard_yds_line) / 40))) * 100, 2)
    std_under_prob = round(100 - std_over_prob, 2)
    alt_over_prob = round((1 - math.exp(-((avg_yds - alt_yds_line) / 40))) * 100, 2)

    # TD Under Probability using Binomial Model (for exactly 0 or 1 TDs)
    prob_0 = binomial_probability(0, int(n_attempts), p_per_attempt)
    prob_1 = binomial_probability(1, int(n_attempts), p_per_attempt)
    under_tds_prob = round((prob_0 + prob_1) * 100, 2)

    props = [
        {"Prop": f"Standard Over", "True Prob": std_over_prob, "Odds": odds_over_std},
        {"Prop": f"Standard Under", "True Prob": std_under_prob, "Odds": odds_under_std},
        {"Prop": f"Alt Over", "True Prob": alt_over_prob, "Odds": odds_alt_over},
        {"Prop": f"Under 1.5 TDs", "True Prob": under_tds_prob, "Odds": odds_under_tds},
    ]

    # Format Results
    results = []
    for prop in props:
        true_p = prop["True Prob"]
        implied_p = round(implied_prob(prop["Odds"]) * 100, 2)
        ev = ev_calc(true_p / 100, prop["Odds"])
        tier = get_tier(true_p)
        results.append({
            "Prop": prop["Prop"],
            "True Probability": f"{true_p}%",
            "Implied Probability": f"{implied_p}%",
            "EV %": f"{ev}%",
            "Tier": tier
        })

    st.dataframe(results)
