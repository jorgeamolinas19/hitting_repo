# Main Streamlit application (modernized UI + live MLB data support)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Ensure current folder is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from legacy.HittingAnalytics import HittingAnalytics
import data_provider

# Page configuration
st.set_page_config(
    page_title="Hitting Analytics Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern/futuristic custom CSS
st.markdown(
    """
    <style>
    /* Gradient header */
    .app-header {
        background: linear-gradient(90deg, #0f172a 0%, #1f2937 40%, #0f172a 100%);
        color: #e6f0ff;
        padding: 18px 30px;
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .app-title {
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        font-weight: 700;
        letter-spacing: 1px;
        font-size: 28px;
    }

    .accent {
        color: #7dd3fc;
    }

    .card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(125,211,252,0.08);
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.5);
    }

    .metric-value {
        font-size: 20px;
        font-weight: 700;
    }

    /* remove Streamlit default footer link area if present */
    footer {visibility: hidden;}
    """,
    unsafe_allow_html=True
)

# Initialize analytics engine
if 'analytics' not in st.session_state:
    st.session_state.analytics = HittingAnalytics()

# Data provider instance
provider = data_provider.DataProvider()

# Sidebar - controls
with st.sidebar:
    st.markdown("## Filters")
    use_live = st.checkbox("Use live MLB data", value=False)
    st.markdown("---")
    if use_live:
        # load teams lazily
        teams = provider.get_teams()
        team = st.selectbox("Select Team", options=["All Teams"] + teams)
        if team != "All Teams":
            players = provider.get_roster(team)
        else:
            # limited list from all teams to avoid long loading times
            players = provider.get_top_players(limit=200)
    else:
        team = st.selectbox("Select Team", ["Team A", "Team B", "Team C"])    
        players = ["Player 1", "Player 2", "Player 3"]

    player = st.selectbox("Select Player", players)
    st.markdown("---")
    st.markdown("### Options")
    season = st.selectbox("Season", options=[2024, 2023, 2022, 2021])
    demo_mode = st.checkbox("Demo mode (cached sample data)", value=False)

# Header
st.markdown(f"<div class='app-header'><div class='app-title'>⚾ <span class='accent'>Hitting</span> Analytics</div></div>", unsafe_allow_html=True)

# Layout: two columns
left_col, right_col = st.columns((1, 2))

with left_col:
    st.markdown("""
    <div class='card'>
    <h4>Quick Summary</h4>
    """, unsafe_allow_html=True)
    # Metrics (live or placeholder)
    if use_live and player and not demo_mode:
        pid = provider.search_player_id(player)
        if pid:
            stats = provider.get_player_stats(pid, season=season)
            avg = stats.get('avg', '—')
            obp = stats.get('obp', '—')
            slg = stats.get('slg', '—')
            hr = stats.get('homeRuns', '—')
            rbi = stats.get('rbi', '—')
        else:
            avg = obp = slg = hr = rbi = '—'
    else:
        # Use analytics engine for demo placeholders
        avg = st.session_state.analytics.calculate_batting_average(50, 150)
        obp = st.session_state.analytics.calculate_obp(50, 10, 0, 150, 2)
        slg = st.session_state.analytics.calculate_slugging_percentage(30, 10, 0, 10, 150)
        hr = 10
        rbi = 45

    st.metric(label="AVG", value=str(avg))
    st.metric(label="OBP", value=str(obp))
    st.metric(label="SLG", value=str(slg))
    st.markdown(f"<p>HR: <strong>{hr}</strong> &nbsp;&nbsp; RBI: <strong>{rbi}</strong></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h4>Controls</h4>
    <p>Use the controls to switch between demo and live data. Player names and team selectors are preserved.</p>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class='card'>
    <h3>Player Details</h3>
    """, unsafe_allow_html=True)

    if use_live and player and not demo_mode:
        pid = provider.search_player_id(player)
        if pid:
            stats = provider.get_player_stats(pid, season=season)
            # Display a small table of stats
            df = pd.DataFrame([stats])
            st.dataframe(df.T, width=800)

            # Create a simple interactive chart (AVG over months example if available)
            if 'monthly' in stats and stats['monthly'] is not None:
                mdf = pd.DataFrame(stats['monthly'])
                fig = px.line(mdf, x='month', y='avg', title=f"Monthly AVG — {player}", markers=True)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Live data: player not found via search — try another name or disable live data.")
    else:
        st.write("Placeholder player profile. Toggle 'Use live MLB data' to fetch real stats.")
        # example chart with random sample data
        sample = pd.DataFrame({
            'game': list(range(1, 11)),
            'avg': [0.250, 0.260, 0.245, 0.270, 0.280, 0.290, 0.300, 0.295, 0.305, 0.310]
        })
        fig = px.line(sample, x='game', y='avg', title=f"Recent AVG — {player}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer note — no link to GitHub
st.markdown("<div style='text-align:right; color:#8892a6; margin-top:18px;'>Built with ♥ — Hitting Analytics</div>", unsafe_allow_html=True)
