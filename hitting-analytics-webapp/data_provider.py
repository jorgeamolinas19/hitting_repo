"""
Data provider for Hitting Analytics.

This module uses pybaseball when available to fetch MLB data. If pybaseball is not installed or fails,
it falls back to the public MLB Stats API via requests.

Functions provided:
- get_teams()
- get_roster(team_name)
- get_top_players(limit)
- search_player_id(name)
- get_player_stats(player_id, season)

"""

from typing import List, Dict, Optional

# Try to use pybaseball first
try:
    from pybaseball import statcast, playerid_lookup, batting_stats, team_roster
    PYBASEBALL_AVAILABLE = True
except Exception:
    PYBASEBALL_AVAILABLE = False

import requests

MLB_API = "https://statsapi.mlb.com/api/v1"

class DataProvider:
    def __init__(self):
        # cache small in-memory maps
        self._teams = None
        self._player_index = {}

    def get_teams(self) -> List[str]:
        if self._teams is not None:
            return self._teams

        if PYBASEBALL_AVAILABLE:
            try:
                # pybaseball does not provide a simple teams list function in all versions, fall back to MLB API
                pass
            except Exception:
                pass

        # Fallback to MLB API
        r = requests.get(f"{MLB_API}/teams?sportId=1")
        r.raise_for_status()
        teams = [t['name'] for t in r.json().get('teams', [])]
        self._teams = teams
        return teams

    def get_roster(self, team_name: str) -> List[str]:
        # find team id
        teams = requests.get(f"{MLB_API}/teams?sportId=1").json().get('teams', [])
        team_id = None
        for t in teams:
            if t['name'] == team_name:
                team_id = t['id']
                break
        if not team_id:
            return []

        r = requests.get(f"{MLB_API}/teams/{team_id}/roster?season=2024")
        r.raise_for_status()
        roster = r.json().get('roster', [])
        names = [p['person']['fullName'] for p in roster]
        # cache id mapping
        for p in roster:
            pid = p['person']['id']
            name = p['person']['fullName']
            self._player_index[name] = pid
        return names

    def get_top_players(self, limit: int = 200) -> List[str]:
        # use league batting stats endpoint to get top players for the season
        try:
            r = requests.get(f"{MLB_API}/stats/leaders?season=2024&sportIds=1&leaderCategories=batting")
            r.raise_for_status()
            # structure can vary, fall back to combined rosters
        except Exception:
            # build from team rosters (may be slower)
            teams = self.get_teams()
            players = []
            for t in teams:
                try:
                    players += self.get_roster(t)
                except Exception:
                    continue
            return players[:limit]

        # If the above worked, try to extract names
        data = r.json()
        # fallback: return flattened team rosters
        teams = self.get_teams()
        players = []
        for t in teams:
            try:
                players += self.get_roster(t)
            except Exception:
                continue
        return players[:limit]

    def search_player_id(self, name: str) -> Optional[int]:
        # direct lookup in our cache
        if name in self._player_index:
            return self._player_index[name]

        # try pybaseball lookup if available
        if PYBASEBALL_AVAILABLE:
            try:
                df = playerid_lookup(last=name.split()[-1], first=name.split()[0])
                if not df.empty:
                    pid = int(df.iloc[0]['key_mlbam'])
                    self._player_index[name] = pid
                    return pid
            except Exception:
                pass

        # fallback: query MLB search endpoint
        r = requests.get(f"{MLB_API}/people/search", params={"query": name})
        if r.status_code == 200:
            res = r.json()
            people = res.get('people', [])
            if people:
                pid = people[0].get('id')
                if pid:
                    self._player_index[name] = pid
                    return pid
        return None

    def get_player_stats(self, player_id: int, season: int = 2024) -> Dict:
        # Try pybaseball batting_stats if available
        if PYBASEBALL_AVAILABLE:
            try:
                df = batting_stats(year=season)
                # batting_stats returns league table; try to find player by id (might not contain id)
            except Exception:
                pass

        # Fallback: use MLB People stats endpoint
        r = requests.get(f"{MLB_API}/people/{player_id}/stats", params={"stats":"season", "season": season})
        if r.status_code != 200:
            return {}
        data = r.json()
        splits = data.get('stats', [])
        if not splits:
            return {}
        # stats structure: stats[0]['splits'][0]['stat']
        stat_block = {}
        try:
            stat_block = splits[0].get('splits', [{}])[0].get('stat', {})
        except Exception:
            stat_block = {}

        # Add a placeholder monthly breakdown if available (not always provided)
        # We'll return the raw stat block plus any derived metrics
        result = stat_block.copy()
        # compute avg/obp/slg keys if not present
        if 'avg' not in result and 'hits' in result and 'atBats' in result and result.get('atBats', 0) > 0:
            result['avg'] = round(result.get('hits', 0) / max(1, result.get('atBats', 1)), 3)
        return result


