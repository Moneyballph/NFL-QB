
import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpg;base64,{encoded}');
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def calculate_ev(true_prob, odds):
    if odds.startswith('-'):
        implied_prob = abs(int(odds)) / (abs(int(odds)) + 100)
    else:
        implied_prob = 100 / (int(odds) + 100)
    ev = (true_prob - implied_prob) * 100
    return round(true_prob * 100, 2), round(implied_prob * 100, 2), round(ev, 2)

def classify_tier(ev):
    if ev >= 25:
        return "🟢 Elite"
    elif ev >= 10:
        return "🟡 Strong"
    elif ev >= 0:
        return "🟧 Moderate"
    else:
        return "🔴 Risky"

add_bg_from_local("background.jpg")

st.title("🏈 Moneyball Phil: NFL Prop Simulator")
st.subheader("Simulate Under 1.5 Passing TDs and Alt Over Passing Yards for any QB")

# Input section
qb_name = st.text_input("Quarterback Name")
opp_team = st.text_input("Opponent Team")

st.subheader("📊 Passing Yards Props")
yards_line = st.number_input("Standard Passing Yards Line", value=225)
odds_over_std = st.text_input("Odds for Over (Standard Line)", value="-110")
odds_under_std = st.text_input("Odds for Under (Standard Line)", value="-105")
alt_yards = st.number_input("Alt Over Yards Line", value=199)
odds_alt = st.text_input("Odds for Alt Over Line", value="-145")

st.subheader("🎯 Touchdown Props")
td_line = st.number_input("Passing TD Line", value=1.5)
odds_td_under = st.text_input("Odds for Under TDs", value="100")

st.subheader("📈 QB & Defense Stats")
qb_yds_gm = st.number_input("QB Yards/Game", value=240.0)
qb_td_gm = st.number_input("QB TD/Game", value=1.4)
pass_att = st.number_input("Pass Attempts/Game", value=31.5)
def_yds = st.number_input("Defense Yards Allowed/Game", value=230.0)
def_td = st.number_input("Defense Pass TDs/Game", value=1.2)

if st.button("Simulate Player"):
    st.header("📋 Player Prop Simulation Results")

    results = []

    # Passing Yards - Over
    avg_line = (qb_yds_gm + def_yds) / 2
    std_over_prob, std_over_impl, std_over_ev = calculate_ev(avg_line / yards_line, odds_over_std)
    results.append(("Standard Over", std_over_prob, std_over_impl, std_over_ev, classify_tier(std_over_ev)))

    # Passing Yards - Under
    std_under_prob = 100 - std_over_prob
    std_under_impl = float(odds_under_std[1:]) / (float(odds_under_std[1:]) + 100) * 100 if odds_under_std.startswith('-') else 100 / (float(odds_under_std) + 100) * 100
    std_under_ev = round(std_under_prob - std_under_impl, 2)
    results.append(("Standard Under", std_under_prob, round(std_under_impl, 2), std_under_ev, classify_tier(std_under_ev)))

    # Alt Over
    alt_over_prob, alt_impl, alt_ev = calculate_ev(avg_line / alt_yards, odds_alt)
    results.append(("Alt Over", alt_over_prob, alt_impl, alt_ev, classify_tier(alt_ev)))

    # TDs - Under 1.5
    avg_tds = (qb_td_gm + def_td) / 2
    td_under_prob = round((1.5 - avg_tds) / 1.5 * 100, 2)
    td_under_prob = max(0, min(td_under_prob, 100))
    td_under_impl = float(odds_td_under[1:]) / (float(odds_td_under[1:]) + 100) * 100 if odds_td_under.startswith('-') else 100 / (float(odds_td_under) + 100) * 100
    td_under_ev = round(td_under_prob - td_under_impl, 2)
    results.append(("Under 1.5 TDs", td_under_prob, round(td_under_impl, 2), td_under_ev, classify_tier(td_under_ev)))

    st.table({
        "Prop": [r[0] for r in results],
        "True Probability": [f"{r[1]}%" for r in results],
        "Implied Probability": [f"{r[2]}%" for r in results],
        "EV %": [f"{r[3]}%" for r in results],
        "Tier": [r[4] for r in results]
    })
