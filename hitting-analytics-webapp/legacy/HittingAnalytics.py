"""Core hitting analytics module."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class HittingAnalytics:
    """Main analytics engine for baseball hitting statistics."""
    
    def __init__(self):
        """Initialize the HittingAnalytics engine."""
        self.players_data = {}
        self.teams_data = {}
        self.season = 2024
    
    def calculate_batting_average(self, hits: int, at_bats: int) -> float:
        """Calculate batting average (AVG).
        
        Args:
            hits: Number of hits
            at_bats: Number of at-bats
            
        Returns:
            Batting average (hits/at_bats)
        """
        if at_bats == 0:
            return 0.0
        return round(hits / at_bats, 3)
    
    def calculate_obp(self, hits: int, walks: int, hit_by_pitch: int, 
                      at_bats: int, sacrifice_flies: int) -> float:
        """Calculate On-Base Percentage (OBP).
        
        Args:
            hits: Number of hits
            walks: Number of walks
            hit_by_pitch: Number of times hit by pitch
            at_bats: Number of at-bats
            sacrifice_flies: Number of sacrifice flies
            
        Returns:
            On-Base Percentage
        """
        numerator = hits + walks + hit_by_pitch
        denominator = at_bats + walks + hit_by_pitch + sacrifice_flies
        
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 3)
    
    def calculate_slugging_percentage(self, singles: int, doubles: int, 
                                     triples: int, home_runs: int, 
                                     at_bats: int) -> float:
        """Calculate Slugging Percentage (SLG).
        
        Args:
            singles: Number of singles
            doubles: Number of doubles
            triples: Number of triples
            home_runs: Number of home runs
            at_bats: Number of at-bats
            
        Returns:
            Slugging Percentage
        """
        if at_bats == 0:
            return 0.0
        
        total_bases = singles + (2 * doubles) + (3 * triples) + (4 * home_runs)
        return round(total_bases / at_bats, 3)
    
    def calculate_ops(self, obp: float, slugging: float) -> float:
        """Calculate On-Base Plus Slugging (OPS).
        
        Args:
            obp: On-Base Percentage
            slugging: Slugging Percentage
            
        Returns:
            OPS value
        """
        return round(obp + slugging, 3)
    
    def calculate_babip(self, hits: int, home_runs: int, at_bats: int, 
                       strikeouts: int, sacrifice_flies: int) -> float:
        """Calculate Batting Average on Balls In Play (BABIP).
        
        Args:
            hits: Number of hits
            home_runs: Number of home runs
            at_bats: Number of at-bats
            strikeouts: Number of strikeouts
            sacrifice_flies: Number of sacrifice flies
            
        Returns:
            BABIP value
        """
        numerator = hits - home_runs
        denominator = at_bats - strikeouts - home_runs + sacrifice_flies
        
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 3)
    
    def calculate_woba(self, singles: int, doubles: int, triples: int, 
                      home_runs: int, walks: int, hit_by_pitch: int, 
                      at_bats: int, sacrifice_flies: int) -> float:
        """Calculate Weighted On-Base Average (wOBA).
        
        Args:
            singles: Number of singles
            doubles: Number of doubles
            triples: Number of triples
            home_runs: Number of home runs
            walks: Number of walks
            hit_by_pitch: Number of times hit by pitch
            at_bats: Number of at-bats
            sacrifice_flies: Number of sacrifice flies
            
        Returns:
            wOBA value
        """
        # 2024 woba weights (approximate)
        weights = {
            'single': 0.89,
            'double': 1.27,
            'triple': 1.62,
            'home_run': 2.10,
            'walk': 0.69,
            'hit_by_pitch': 0.72
        }
        
        numerator = (weights['single'] * singles + 
                    weights['double'] * doubles +
                    weights['triple'] * triples +
                    weights['home_run'] * home_runs +
                    weights['walk'] * walks +
                    weights['hit_by_pitch'] * hit_by_pitch)
        
        denominator = at_bats + walks + hit_by_pitch + sacrifice_flies
        
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 3)
    
    def get_player_stats(self, player_name: str) -> Optional[Dict]:
        """Retrieve stats for a specific player.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary of player statistics or None if not found
        """
        return self.players_data.get(player_name)
    
    def get_team_stats(self, team_name: str) -> Optional[Dict]:
        """Retrieve stats for a specific team.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Dictionary of team statistics or None if not found
        """
        return self.teams_data.get(team_name)
    
    def add_player_stats(self, player_name: str, stats: Dict) -> None:
        """Add or update player statistics.
        
        Args:
            player_name: Name of the player
            stats: Dictionary of player statistics
        """
        self.players_data[player_name] = stats
    
    def add_team_stats(self, team_name: str, stats: Dict) -> None:
        """Add or update team statistics.
        
        Args:
            team_name: Name of the team
            stats: Dictionary of team statistics
        """
        self.teams_data[team_name] = stats
