
import streamlit as st

st.set_page_config(page_title="Moneyball Phil: NFL Prop Simulator", layout="centered")
st.title("🏈 Moneyball Phil: NFL Prop Simulator (v1 Final)")
st.markdown("Simulate **Under 1.5 Passing TDs**, **Standard Passing Yards Over/Under**, and **Alt Over Passing Yards** based on stats.")

# Inputs
qb_name = st.text_input("Quarterback Name")
opp_team = st.text_input("Opponent Team")

st.subheader("📏 Standard Passing Yards Line")
pass_yards_line = st.number_input("Passing Yards Line", value=225)
pass_yards_over_odds = st.number_input("Odds for Over", value=-110)
pass_yards_under_odds = st.number_input("Odds for Under", value=-110)

st.subheader("🟩 Alt Over Passing Yards Line")
alt_yards_line = st.number_input("Alt Over Yards Line", value=199)
alt_yards_odds = st.number_input("Odds for Alt Over", value=-145)

st.subheader("🔴 Passing TD Line")
td_line = st.number_input("Passing TD Line", value=1.5)
td_under_odds = st.number_input("Odds for Under TDs", value=100)

st.subheader("📊 QB Stats")
qb_yards_pg = st.number_input("QB Yards/Game", value=240)
qb_td_pg = st.number_input("QB TD/Game", value=1.4)
pass_att_pg = st.number_input("Pass Attempts/Game", value=31.5)

st.subheader("🛡️ Defense Stats")
def_yards_allowed_pg = st.number_input("Defense Yards Allowed/Game", value=230)
def_td_allowed_pg = st.number_input("Defense Pass TDs/Game", value=1.2)

# Calculate probabilities
if st.button("Simulate Player"):
    avg_yards = (qb_yards_pg + def_yards_allowed_pg) / 2
    std_ovr_prob = max(0, min(1, 1 - (pass_yards_line - avg_yards) / 100))
    std_und_prob = 1 - std_ovr_prob

    std_ovr_imp = abs(pass_yards_over_odds) / (abs(pass_yards_over_odds) + 100) if pass_yards_over_odds < 0 else 100 / (pass_yards_over_odds + 100)
    std_und_imp = abs(pass_yards_under_odds) / (abs(pass_yards_under_odds) + 100) if pass_yards_under_odds < 0 else 100 / (pass_yards_under_odds + 100)
    std_ovr_ev = (std_ovr_prob - std_ovr_imp) * 100
    std_und_ev = (std_und_prob - std_und_imp) * 100

    alt_ovr_prob = max(0, min(1, 1 - (alt_yards_line - avg_yards) / 100))
    alt_ovr_imp = abs(alt_yards_odds) / (abs(alt_yards_odds) + 100) if alt_yards_odds < 0 else 100 / (alt_yards_odds + 100)
    alt_ovr_ev = (alt_ovr_prob - alt_ovr_imp) * 100

    avg_td = (qb_td_pg + def_td_allowed_pg) / 2
    td_under_prob = max(0, min(1, 1.5 - avg_td))
    td_under_imp = abs(td_under_odds) / (abs(td_under_odds) + 100) if td_under_odds < 0 else 100 / (td_under_odds + 100)
    td_under_ev = (td_under_prob - td_under_imp) * 100

    def tier(p):
        return "🟦 Elite" if p >= 0.8 else "🟩 Strong" if p >= 0.7 else "🟨 Moderate" if p >= 0.6 else "🔴 Risky"

    st.markdown(f"### 📊 Simulation Results for {qb_name} vs {opp_team}")
    st.markdown(f"""
| Prop | True Probability | Implied Probability | EV % | Tier |
|------|------------------|----------------------|------|------|
| **Over {pass_yards_line} Yards** | {std_ovr_prob:.2%} | {std_ovr_imp:.2%} | {std_ovr_ev:.2f}% | {tier(std_ovr_prob)} |
| **Under {pass_yards_line} Yards** | {std_und_prob:.2%} | {std_und_imp:.2%} | {std_und_ev:.2f}% | {tier(std_und_prob)} |
| **Alt Over {alt_yards_line} Yards** | {alt_ovr_prob:.2%} | {alt_ovr_imp:.2%} | {alt_ovr_ev:.2f}% | {tier(alt_ovr_prob)} |
| **Under {td_line} Passing TDs** | {td_under_prob:.2%} | {td_under_imp:.2%} | {td_under_ev:.2f}% | {tier(td_under_prob)} |
""")
