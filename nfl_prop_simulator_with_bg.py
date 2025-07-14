
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

add_bg_from_local("background.jpg")

st.title("🏈 Moneyball Phil: NFL Prop Simulator")
st.subheader("Simulate Under 1.5 Passing TDs and Alt Over Passing Yards for any QB")

# Input section
st.text_input("Quarterback Name", key="qb_name")
st.text_input("Opponent Team", key="opp_team")

st.subheader("📊 Passing Yards Props")
st.number_input("Standard Passing Yards Line", value=225, key="yards_line")
st.text_input("Odds for Over (Standard Line)", value="-110", key="odds_over_std")
st.text_input("Odds for Under (Standard Line)", value="-105", key="odds_under_std")
st.number_input("Alt Over Yards Line", value=199, key="alt_yards")
st.text_input("Odds for Alt Over Line", value="-145", key="odds_alt")

st.subheader("🎯 Touchdown Props")
st.number_input("Passing TD Line", value=1.5, key="td_line")
st.text_input("Odds for Under TDs", value="100", key="odds_td_under")

st.subheader("📈 QB & Defense Stats")
st.number_input("QB Yards/Game", value=240.0, key="qb_yds_gm")
st.number_input("QB TD/Game", value=1.4, key="qb_td_gm")
st.number_input("Pass Attempts/Game", value=31.5, key="pass_att")
st.number_input("Defense Yards Allowed/Game", value=230.0, key="def_yds")
st.number_input("Defense Pass TDs/Game", value=1.2, key="def_td")

if st.button("Simulate Player"):
    st.success("Simulation logic placeholder - working version runs simulations and displays EV and tiers.")
