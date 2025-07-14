
import streamlit as st
import math

st.set_page_config(page_title="NFL Prop Simulator (v1)", layout="wide")
st.title("🏈 Moneyball Phil: NFL Prop Simulator (v1)")
st.markdown("Simulate **Under 1.5 Passing TDs** and **Alt Over Passing Yards** for any QB based on historical or projected stats.")

# QB Info Inputs
qb_name = st.text_input("Quarterback Name")
opponent = st.text_input("Opponent Team")
yd_line = st.number_input("Passing Yards Line", value=225)
yd_odds = st.number_input("Odds for Passing Yards Line", value=-110)
alt_yd_line = st.number_input("Alt Over Yards Line", value=199)
alt_yd_odds = st.number_input("Odds for Alt Over Line", value=-145)
td_line = st.selectbox("Passing TD Line", [1.5, 2.5], index=0)
td_odds = st.number_input("Odds for Under TDs", value=100)

# QB Stats
ypg = st.number_input("QB Yards/Game", value=240)
tdpg = st.number_input("QB TD/Game", value=1.4)
attpg = st.number_input("Pass Attempts/Game", value=31.5)

# Defense Stats
def_yd_allow = st.number_input("Defense Yards Allowed/Game", value=230)
def_td_allow = st.number_input("Defense Pass TDs/Game", value=1.2)

# Simulate Button
if st.button("Simulate Props"):
    # True Probabilities (simple model for demonstration)
    def calc_prob(over_avg, line):
        z = (line - over_avg) / 25  # basic variance
        prob = 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))
        return round(prob * 100, 2)

    # Alt Over Passing Yards
    alt_over_true = calc_prob(ypg, alt_yd_line)
    implied_alt = round(100 / (alt_yd_odds + 100) * 100 if alt_yd_odds > 0 else abs(alt_yd_odds) / (abs(alt_yd_odds) + 100) * 100, 2)
    ev_alt = round(alt_over_true - implied_alt, 2)

    # Under Passing TDs
    under_td_true = calc_prob(tdpg, td_line)
    implied_td = round(100 / (td_odds + 100) * 100 if td_odds > 0 else abs(td_odds) / (abs(td_odds) + 100) * 100, 2)
    ev_td = round(under_td_true - implied_td, 2)

    # Tier function
    def tier(ev):
        if ev >= 15:
            return "🟢 Elite"
        elif ev >= 10:
            return "🟡 Strong"
        elif ev >= 5:
            return "🟠 Moderate"
        else:
            return "🔴 Risky"

    # Display Results
    st.subheader(f"📊 Sim Results for {qb_name} vs {opponent}")
    st.markdown("### Passing Yards (Alt Line)")
    st.write(f"**Line:** {alt_yd_line} @ {alt_yd_odds}")
    st.write(f"**True Probability:** {alt_over_true}%")
    st.write(f"**Implied Probability:** {implied_alt}%")
    st.write(f"**EV%:** {ev_alt}%")
    st.write(f"**Tier:** {tier(ev_alt)}")

    st.markdown("### Passing TDs (Under)")
    st.write(f"**Line:** Under {td_line} @ {td_odds}")
    st.write(f"**True Probability:** {under_td_true}%")
    st.write(f"**Implied Probability:** {implied_td}%")
    st.write(f"**EV%:** {ev_td}%")
    st.write(f"**Tier:** {tier(ev_td)}")
