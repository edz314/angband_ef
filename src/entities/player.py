"""
src/entities/player.py
Core player entity handling stats, action points, equipment, and inventory.
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class EquipmentSlot:
    slot_name: str  # e.g., "hands", "neck", "eyes", "wrists"
    item_id: Optional[str] = None
    condition: float = 100.0  # Percentage degradation

@dataclass
class Player:
    name: str = "Wanderer"
    
    # Core Stats
    hp: int = 100
    max_hp: int = 100
    
    stamina: int = 100
    max_stamina: int = 100
    
    pleasure: int = 0
    max_pleasure: int = 100
    
    # Affinities (Meta progression modifiers)
    dominance_affinity: int = 0
    submission_affinity: int = 0
    
    # Action Points
    ap: int = 5
    max_ap: int = 5
    
    # Equipment & Inventory
    equipment: Dict[str, EquipmentSlot] = field(default_factory=lambda: {
        "hands": EquipmentSlot("hands"),
        "neck": EquipmentSlot("neck"),
        "eyes": EquipmentSlot("eyes"),
        "wrists": EquipmentSlot("wrists")
    })
    inventory: List[Dict] = field(default_factory=list)  # Stores item dicts
    
    # State Flags
    is_restrained: bool = False
    blindfolded: bool = False
    gagged: bool = False
    
    def apply_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        
    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)
        
    def gain_pleasure(self, amount: int) -> None:
        self.pleasure = min(self.max_pleasure, self.pleasure + amount)
        if self.pleasure >= 90 and not getattr(self, 'overloaded', False):
            self.overloaded = True
            
    def gain_stamina(self, amount: int) -> None:
        self.stamina = min(self.max_stamina, self.stamina + amount)
        
    def spend_ap(self, cost: int) -> bool:
        if self.ap >= cost:
            self.ap -= cost
            return True
        return False
        
    def regenerate_ap(self, base_amount: int = 5) -> None:
        # Affinity modifiers affect AP regen slightly
        dom_bonus = max(0, self.dominance_affinity // 20)
        sub_bonus = max(0, self.submission_affinity // 20)
        total = base_amount + dom_bonus + sub_bonus
        self.ap = min(self.max_ap, self.ap + total)
        
    def equip_item(self, slot: str, item_dict: Dict) -> bool:
        if slot in self.equipment:
            self.equipment[slot].item_id = item_dict.get("id")
            self.equipment[slot].condition = 100.0
            # Apply immediate stat modifiers from item
            for stat, val in item_dict.get("modifiers", {}).items():
                if hasattr(self, stat):
                    current = getattr(self, stat)
                    setattr(self, stat, current + val)
            return True
        return False
        
    def degrade_equipment(self, slot: str, amount: float) -> None:
        if slot in self.equipment:
            self.equipment[slot].condition -= amount
            if self.equipment[slot].condition <= 0:
                # Item breaks
                old_id = self.equipment[slot].item_id
                self.equipment[slot] = EquipmentSlot(slot)
                return old_id
        return None
        
    def is_alive(self) -> bool:
        return self.hp > 0

# requirements.txt
textual>=0.40.0      # Modern TUI framework for terminal rendering
httpx>=0.25.0        # Async HTTP client for LLM API calls
pyyaml>=6.0          # Configuration management
jinja2>=3.1.2        # Prompt template engine
rich>=13.7.0         # Console formatting (fallback/compatibility)
