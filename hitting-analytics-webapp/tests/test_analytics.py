"""Tests for HittingAnalytics module."""

import pytest
from legacy.HittingAnalytics import HittingAnalytics


@pytest.fixture
def analytics():
    """Fixture to provide HittingAnalytics instance."""
    return HittingAnalytics()


class TestBattingAverage:
    """Tests for batting average calculation."""
    
    def test_batting_average_calculation(self, analytics):
        """Test basic batting average calculation."""
        avg = analytics.calculate_batting_average(hits=120, at_bats=400)
        assert avg == 0.300
    
    def test_batting_average_zero_at_bats(self, analytics):
        """Test batting average with zero at-bats."""
        avg = analytics.calculate_batting_average(hits=0, at_bats=0)
        assert avg == 0.0
    
    def test_batting_average_perfect(self, analytics):
        """Test perfect batting average."""
        avg = analytics.calculate_batting_average(hits=10, at_bats=10)
        assert avg == 1.0


class TestOBP:
    """Tests for On-Base Percentage calculation."""
    
    def test_obp_calculation(self, analytics):
        """Test basic OBP calculation."""
        obp = analytics.calculate_obp(
            hits=120, walks=40, hit_by_pitch=5,
            at_bats=400, sacrifice_flies=2
        )
        assert obp == 0.367
    
    def test_obp_zero_denominator(self, analytics):
        """Test OBP with zero denominator."""
        obp = analytics.calculate_obp(
            hits=0, walks=0, hit_by_pitch=0,
            at_bats=0, sacrifice_flies=0
        )
        assert obp == 0.0


class TestSlugging:
    """Tests for Slugging Percentage calculation."""
    
    def test_slugging_percentage(self, analytics):
        """Test slugging percentage calculation."""
        slug = analytics.calculate_slugging_percentage(
            singles=80, doubles=25, triples=2,
            home_runs=20, at_bats=400
        )
        expected = round((80 + 50 + 6 + 80) / 400, 3)
        assert slug == expected
    
    def test_slugging_percentage_zero_at_bats(self, analytics):
        """Test slugging with zero at-bats."""
        slug = analytics.calculate_slugging_percentage(
            singles=0, doubles=0, triples=0,
            home_runs=0, at_bats=0
        )
        assert slug == 0.0


class TestOPS:
    """Tests for OPS calculation."""
    
    def test_ops_calculation(self, analytics):
        """Test OPS calculation."""
        ops = analytics.calculate_ops(obp=0.367, slugging=0.500)
        assert ops == 0.867


class TestBABIP:
    """Tests for BABIP calculation."""
    
    def test_babip_calculation(self, analytics):
        """Test BABIP calculation."""
        babip = analytics.calculate_babip(
            hits=120, home_runs=20, at_bats=400,
            strikeouts=80, sacrifice_flies=2
        )
        expected = round((120 - 20) / (400 - 80 - 20 + 2), 3)
        assert babip == expected


class TestWOBA:
    """Tests for wOBA calculation."""
    
    def test_woba_calculation(self, analytics):
        """Test wOBA calculation."""
        woba = analytics.calculate_woba(
            singles=80, doubles=25, triples=2,
            home_runs=20, walks=40, hit_by_pitch=5,
            at_bats=400, sacrifice_flies=2
        )
        assert isinstance(woba, float)
        assert 0 <= woba <= 1.0


class TestPlayerStats:
    """Tests for player statistics management."""
    
    def test_add_player_stats(self, analytics):
        """Test adding player statistics."""
        stats = {'avg': 0.300, 'hr': 30, 'rbi': 100}
        analytics.add_player_stats('John Doe', stats)
        retrieved = analytics.get_player_stats('John Doe')
        assert retrieved == stats
    
    def test_get_nonexistent_player(self, analytics):
        """Test retrieving nonexistent player."""
        result = analytics.get_player_stats('Nonexistent Player')
        assert result is None


class TestTeamStats:
    """Tests for team statistics management."""
    
    def test_add_team_stats(self, analytics):
        """Test adding team statistics."""
        stats = {'avg': 0.270, 'hr': 150, 'rbi': 800}
        analytics.add_team_stats('Team A', stats)
        retrieved = analytics.get_team_stats('Team A')
        assert retrieved == stats
    
    def test_get_nonexistent_team(self, analytics):
        """Test retrieving nonexistent team."""
        result = analytics.get_team_stats('Nonexistent Team')
        assert result is None
