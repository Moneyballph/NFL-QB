
import streamlit as st

st.set_page_config(page_title="Moneyball Phil: NFL Prop Simulator", layout="centered")

st.title("🏈 Moneyball Phil: NFL Prop Simulator (v2)")
st.markdown("Simulate Under 1.5 Passing TDs and Alt Over/Standard Passing Yards for any QB based on stats.")

# Inputs
qb_name = st.text_input("Quarterback Name")
opponent = st.text_input("Opponent Team")

st.subheader("📊 Passing Yards Props")
standard_yds_line = st.number_input("Standard Passing Yards Line", value=225)
std_yds_odds_over = st.number_input("Odds for Over (Standard Line)", value=-110)
std_yds_odds_under = st.number_input("Odds for Under (Standard Line)", value=-110)

alt_yds_line = st.number_input("Alt Over Yards Line", value=199)
alt_yds_odds = st.number_input("Odds for Alt Over Line", value=-145)

st.subheader("🎯 Touchdown Props")
td_line = st.number_input("Passing TD Line", value=1.5)
td_under_odds = st.number_input("Odds for Under TDs", value=100)

st.subheader("📈 QB & Defense Stats")
qb_yds_game = st.number_input("QB Yards/Game", value=240.0)
qb_tds_game = st.number_input("QB TD/Game", value=1.4)
pass_att_game = st.number_input("Pass Attempts/Game", value=31.5)
def_yds_allow = st.number_input("Defense Yards Allowed/Game", value=230.0)
def_tds_allow = st.number_input("Defense Pass TDs/Game", value=1.2)

def implied_prob(odds):
    return abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)

def ev(true_prob, odds):
    implied = implied_prob(odds)
    return round((true_prob - implied) * 100, 2)

def tier(prob):
    if prob >= 80:
        return "🟢 Elite"
    elif prob >= 70:
        return "🟩 Strong"
    elif prob >= 60:
        return "🟨 Moderate"
    else:
        return "🔴 Risky"

if st.button("Simulate Player"):
    results = []

    # Standard Passing Yards
    over_std_prob = round(100 - ((standard_yds_line - qb_yds_game) / qb_yds_game) * 100, 2)
    under_std_prob = round(100 - over_std_prob, 2)
    ev_std_over = ev(over_std_prob / 100, std_yds_odds_over)
    ev_std_under = ev(under_std_prob / 100, std_yds_odds_under)

    results.append(["Standard Over", f"{over_std_prob}%", f"{implied_prob(std_yds_odds_over)*100:.2f}%", f"{ev_std_over}%", tier(over_std_prob)])
    results.append(["Standard Under", f"{under_std_prob}%", f"{implied_prob(std_yds_odds_under)*100:.2f}%", f"{ev_std_under}%", tier(under_std_prob)])

    # Alt Over
    alt_prob = round(100 - ((alt_yds_line - qb_yds_game) / qb_yds_game) * 100, 2)
    ev_alt = ev(alt_prob / 100, alt_yds_odds)
    results.append(["Alt Over", f"{alt_prob}%", f"{implied_prob(alt_yds_odds)*100:.2f}%", f"{ev_alt}%", tier(alt_prob)])

    # TDs Under
    td_prob = round(100 - ((td_line - qb_tds_game) / qb_tds_game) * 100, 2)
    ev_td = ev(td_prob / 100, td_under_odds)
    results.append(["Under TDs", f"{td_prob}%", f"{implied_prob(td_under_odds)*100:.2f}%", f"{ev_td}%", tier(td_prob)])

    st.subheader("📋 Player Prop Simulation Results")
    st.table(
        {
            "Prop": [r[0] for r in results],
            "True Probability": [r[1] for r in results],
            "Implied Probability": [r[2] for r in results],
            "EV %": [r[3] for r in results],
            "Tier": [r[4] for r in results],
        }
    )
