
import streamlit as st

def calculate_implied_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)

def calculate_ev(true_prob, implied_prob):
    return (true_prob - implied_prob) * 100

st.set_page_config(page_title="NFL Prop Simulator v2", layout="centered")

st.title("🏈 NFL Prop Simulator (v2)")
st.subheader("Dual-Direction Evaluation for Passing Yards")

with st.form("input_form"):
    qb_name = st.text_input("Quarterback Name")
    passing_yards_line = st.number_input("Passing Yards Line", min_value=0)
    over_odds = st.number_input("Odds for Over", value=-110)
    under_odds = st.number_input("Odds for Under", value=-110)
    true_over_prob = st.slider("Simulated True Probability of Over (%)", 0.0, 100.0, 65.0)
    submitted = st.form_submit_button("Simulate Player")

if submitted:
    true_under_prob = 100 - true_over_prob
    implied_over = calculate_implied_probability(over_odds) * 100
    implied_under = calculate_implied_probability(under_odds) * 100

    ev_over = calculate_ev(true_over_prob, implied_over)
    ev_under = calculate_ev(true_under_prob, implied_under)

    def tier(ev):
        if ev >= 20:
            return "🟢 Elite"
        elif ev >= 10:
            return "🟡 Strong"
        elif ev >= 0:
            return "🟠 Moderate"
        else:
            return "🔴 Risky"

    st.markdown("### 🧠 Results:")
    st.table({
        "Direction": ["Over", "Under"],
        "True Prob (%)": [round(true_over_prob, 2), round(true_under_prob, 2)],
        "Implied Prob (%)": [round(implied_over, 2), round(implied_under, 2)],
        "EV (%)": [round(ev_over, 2), round(ev_under, 2)],
        "Tier": [tier(ev_over), tier(ev_under)]
    })
