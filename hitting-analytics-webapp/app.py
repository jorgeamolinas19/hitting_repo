# Main Streamlit application
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from legacy.HittingAnalytics import HittingAnalytics

# Page configuration
st.set_page_config(
    page_title="Hitting Analytics Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("⚾ Hitting Analytics Dashboard")
    st.markdown("---")
    
    # Initialize session state
    if 'analytics' not in st.session_state:
        st.session_state.analytics = HittingAnalytics()
    
    # Sidebar navigation
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Player Analysis", "Team Comparison", "Advanced Metrics"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Player Analysis":
        show_player_analysis()
    elif page == "Team Comparison":
        show_team_comparison()
    elif page == "Advanced Metrics":
        show_advanced_metrics()

def show_overview():
    st.header("Dashboard Overview")
    st.write("Welcome to the Hitting Analytics Dashboard. Select a page from the sidebar to explore baseball statistics.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Players", "30")
    with col2:
        st.metric("Active Games", "15")
    with col3:
        st.metric("Season", "2024")

def show_player_analysis():
    st.header("Player Analysis")
    st.write("Analyze individual player statistics and performance metrics.")
    
    player_name = st.selectbox(
        "Select a Player",
        ["Player 1", "Player 2", "Player 3"]
    )
    
    st.subheader(f"Stats for {player_name}")
    # Placeholder for player stats
    st.write("Player statistics would be displayed here.")

def show_team_comparison():
    st.header("Team Comparison")
    st.write("Compare hitting statistics across teams.")
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team 1", ["Team A", "Team B", "Team C"])
    with col2:
        team2 = st.selectbox("Select Team 2", ["Team B", "Team A", "Team C"])
    
    st.write(f"Comparing {team1} vs {team2}")

def show_advanced_metrics():
    st.header("Advanced Metrics")
    st.write("Explore advanced baseball analytics and derived metrics.")
    
    metric_type = st.multiselect(
        "Select Metrics",
        ["WAR", "wOBA", "BABIP", "Exit Velocity"]
    )
    
    if metric_type:
        st.write(f"Displaying: {', '.join(metric_type)}")

if __name__ == "__main__":
    main()
