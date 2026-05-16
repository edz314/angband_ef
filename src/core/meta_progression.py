"""
src/core/meta_progression.py
Manages persistent upgrades across runs (permadeath loop).
"""
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MetaProgression:
    """Persistent state saved between runs."""
    run_count: int = 0
    total_districts_explored: set = field(default_factory=set)
    unlocked_districts: List[str] = field(default_factory=lambda: ["oracle"]) # Start with Oracle
    passive_perks: Dict[str, int] = field(default_factory=dict) # e.g., {"iron_lung": 1}
    
    def load(self, path: str) -> None:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    self.run_count = data.get('run_count', 0)
                    self.total_districts_explored = set(data.get('total_districts_explored', []))
                    self.unlocked_districts = data.get('unlocked_districts', ["oracle"])
                    self.passive_perks = data.get('passive_perks', {})
            except (json.JSONDecodeError, IOError):
                pass # Start fresh on error
        
    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump({
                "run_count": self.run_count,
                "total_districts_explored": list(self.total_districts_explored),
                "unlocked_districts": self.unlocked_districts,
                "passive_perks": self.passive_perks
            }, f, indent=2)

    def record_death(self, district_id: str) -> None:
        """Called when player dies."""
        self.run_count += 1
        self.total_districts_explored.add(district_id)
        
        # Unlock logic based on run count or specific achievements
        if self.run_count >= 3 and "station" not in self.unlocked_districts:
            self.unlocked_districts.append("station")
            
    def record_escape(self, district_id: str) -> None:
        """Called when player escapes a district."""
        self.total_districts_explored.add(district_id)
        
    def get_passive_bonus(self, perk_name: str) -> int:
        return self.passive_perks.get(perk_name, 0)
    def get_passive_bonus(self, perk_name: str) -> int:
        return self.passive_perks.get(perk_name, 0)