"""Tests for MLB data integration."""

import pytest
from legacy.HittingAnalytics import HittingAnalytics


@pytest.fixture
def analytics():
    """Fixture to provide HittingAnalytics instance."""
    return HittingAnalytics()


class TestMLBDataIntegration:
    """Tests for MLB data integration."""
    
    def test_season_initialization(self, analytics):
        """Test that season is properly initialized."""
        assert analytics.season == 2024
    
    def test_multiple_player_storage(self, analytics):
        """Test storing multiple players."""
        players = [
            ('Aaron Judge', {'avg': 0.322, 'hr': 58}),
            ('Juan Soto', {'avg': 0.288, 'hr': 41}),
            ('Gerrit Cole', {'avg': 0.0, 'hr': 0})  # Pitcher stats
        ]
        
        for name, stats in players:
            analytics.add_player_stats(name, stats)
        
        for name, stats in players:
            assert analytics.get_player_stats(name) == stats
    
    def test_multiple_team_storage(self, analytics):
        """Test storing multiple teams."""
        teams = [
            ('Yankees', {'avg': 0.264, 'hr': 252}),
            ('Red Sox', {'avg': 0.270, 'hr': 198}),
            ('Rays', {'avg': 0.245, 'hr': 178})
        ]
        
        for name, stats in teams:
            analytics.add_team_stats(name, stats)
        
        for name, stats in teams:
            assert analytics.get_team_stats(name) == stats
    
    def test_stats_persistence(self, analytics):
        """Test that stats persist across multiple retrievals."""
        stats = {'avg': 0.300, 'hr': 30}
        analytics.add_player_stats('Test Player', stats)
        
        # Retrieve multiple times
        result1 = analytics.get_player_stats('Test Player')
        result2 = analytics.get_player_stats('Test Player')
        
        assert result1 == result2
        assert result1 == stats
